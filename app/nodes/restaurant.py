import time
import random

from langchain_core.messages import AIMessage
from Venue_booking_agent.app.models import BookingState
from app.services.email_service import send_email

from Venue_booking_agent.app.config import (
    MAX_RETRIES,
    RETRY_DELAY_SECONDS,
    STATUS_CONFIRMED,
    STATUS_REJECTED,
    STATUS_FAILED_NO_RESPONSE,
)

from Venue_booking_agent.app.services.notification_service import (
    booking_confirmed_message,
    booking_rejected_message,
    booking_failed_message,
)

from Venue_booking_agent.app.services.restaurant_service import get_restaurant_response

from Venue_booking_agent.app.logger import logger

from Venue_booking_agent.app.services.storage_service import save_booking


def send_to_restaurant(state: BookingState):
    booking = state.booking

    booking_id = state.booking_id or f"BK{random.randint(1000, 9999)}"

    retry_count = 0
    max_retries = MAX_RETRIES

    while retry_count < max_retries:
        logger.info("Sending booking request to restaurant")

        print("=" * 50)
        print(f"Booking ID : {booking_id}")
        print(f"Customer   : {booking.name}")
        print(f"Phone      : {booking.phone_number}")
        print(f"Date       : {booking.date}")
        print(f"Time       : {booking.time}")
        print(f"Guests     : {booking.party_size}")
        print(f"Dietary    : {booking.dietary}")
        print("=" * 50)

        response = get_restaurant_response()

        if response == "accept":
            confirmation_message = booking_confirmed_message(
                booking_id,
                booking,
            )

            send_email(
                to_email=booking.email,
                subject=f"Booking Confirmed - {booking_id}",
                body=confirmation_message,
            )

            save_booking(booking_id, booking, STATUS_CONFIRMED)
            return {
                "booking_id": booking_id,
                "booking_status": STATUS_CONFIRMED,
                "messages": [
                    AIMessage(content=confirmation_message)
                ]
            }

        if response == "reject":
            rejection_message = booking_rejected_message(booking_id, booking)

            save_booking(booking_id, booking, STATUS_REJECTED)

            return {
                "booking_id": booking_id,
                "booking_status": STATUS_REJECTED,
                "messages": [
                    AIMessage(content=rejection_message)
                ]
            }

        if response == "hold":
            logger.info("Restaurant placed booking on hold")
            print(f"Checking again in {RETRY_DELAY_SECONDS} seconds...")
            time.sleep(RETRY_DELAY_SECONDS)
            continue

        retry_count += 1

        logger.warning(f"No response received ({retry_count}/{max_retries})")

        if retry_count < max_retries:
            print(f"Retrying in {RETRY_DELAY_SECONDS} seconds...")
            time.sleep(RETRY_DELAY_SECONDS)

    failed_message = booking_failed_message(booking_id, booking, MAX_RETRIES)
    
    save_booking(booking_id, booking, STATUS_FAILED_NO_RESPONSE)

    return {
        "booking_id": booking_id,
        "booking_status": STATUS_FAILED_NO_RESPONSE,
        "messages": [
            AIMessage(content=failed_message)
        ]
    }