# import time
# import random

# from langchain_core.messages import AIMessage

# from app.models import BookingState
# from app.services.email_service import send_email
# from app.services.restaurant_service import get_restaurant_response
# from app.services.storage_service import save_booking
# from app.services.notification_service import (
#     booking_confirmed_message,
#     booking_rejected_message,
#     booking_failed_message,
# )
# from app.services.telegram_service import send_telegram_booking_request
# from app.logger import logger

# from app.config import (
#     MAX_RETRIES,
#     RETRY_DELAY_SECONDS,
#     STATUS_CONFIRMED,
#     STATUS_REJECTED,
#     STATUS_FAILED_NO_RESPONSE,
# )


# def send_to_restaurant(state: BookingState):
#     booking = state.booking
#     restaurant = state.selected_restaurant

#     booking_id = state.booking_id or f"BK{random.randint(1000, 9999)}"

#     retry_count = 0
#     max_retries = MAX_RETRIES

#     while retry_count < max_retries:
#         logger.info("Sending booking request to restaurant")

#         print("\n📤 Sending booking request to restaurant...\n")
#         print("=" * 50)
#         print(f"Booking ID  : {booking_id}")
#         print(f"Restaurant  : {restaurant.name}")
#         print(f"Rest. Phone : {restaurant.phone}")
#         print(f"Customer    : {booking.name}")
#         print(f"User Phone  : {booking.phone_number}")
#         print(f"Email       : {booking.email}")
#         print(f"Date        : {booking.date}")
#         print(f"Time        : {booking.time}")
#         print(f"Guests      : {booking.party_size}")
#         print(f"Dietary     : {booking.dietary}")
#         print("=" * 50)

#         # Send booking request to restaurant Telegram
#         send_telegram_booking_request(
#             booking_id=booking_id,
#             booking=booking,
#             restaurant=restaurant,
#         )

#         print("\n✅ Telegram booking request sent to restaurant.")
#         print("For now, enter restaurant response manually below.")
#         print("Later we will replace this with Telegram button callback response.\n")

#         response = get_restaurant_response()

#         if response == "accept":
#             confirmation_message = booking_confirmed_message(
#                 booking_id=booking_id,
#                 booking=booking,
#                 restaurant=restaurant,
#             )

#             send_email(
#                 to_email=booking.email,
#                 subject=f"Booking Confirmed - {restaurant.name} - {booking_id}",
#                 body=confirmation_message,
#             )

#             save_booking(
#                 booking_id,
#                 booking,
#                 restaurant,
#                 STATUS_CONFIRMED,
#             )

#             return {
#                 "booking_id": booking_id,
#                 "booking_status": STATUS_CONFIRMED,
#                 "messages": [
#                     AIMessage(content=confirmation_message)
#                 ],
#             }

#         if response == "reject":
#             rejection_message = booking_rejected_message(
#                 booking_id=booking_id,
#                 booking=booking,
#                 restaurant=restaurant,
#             )

#             save_booking(
#                 booking_id,
#                 booking,
#                 restaurant,
#                 STATUS_REJECTED,
#             )

#             return {
#                 "booking_id": booking_id,
#                 "booking_status": STATUS_REJECTED,
#                 "messages": [
#                     AIMessage(content=rejection_message)
#                 ],
#             }

#         if response == "hold":
#             logger.info("Restaurant placed booking on hold")
#             print("\n⏳ Restaurant placed booking on HOLD.")
#             print(f"Checking again in {RETRY_DELAY_SECONDS} seconds...")
#             time.sleep(RETRY_DELAY_SECONDS)
#             continue

#         retry_count += 1

#         logger.warning(
#             f"No response received ({retry_count}/{max_retries})"
#         )

#         print(f"\n⚠️ No response received ({retry_count}/{max_retries})")

#         if retry_count < max_retries:
#             print(f"Retrying in {RETRY_DELAY_SECONDS} seconds...")
#             time.sleep(RETRY_DELAY_SECONDS)

#     failed_message = booking_failed_message(
#         booking_id=booking_id,
#         booking=booking,
#         max_retries=MAX_RETRIES,
#         restaurant=restaurant,
#     )

#     save_booking(
#         booking_id,
#         booking,
#         restaurant,
#         STATUS_FAILED_NO_RESPONSE,
#     )

#     return {
#         "booking_id": booking_id,
#         "booking_status": STATUS_FAILED_NO_RESPONSE,
#         "messages": [
#             AIMessage(content=failed_message)
#         ],
#     }


import time
import random

from langchain_core.messages import AIMessage

from app.models import BookingState
from app.services.email_service import send_email
from app.services.storage_service import (
    save_booking,
    get_booking_status,
)
from app.services.notification_service import (
    booking_confirmed_message,
    booking_rejected_message,
    booking_failed_message,
)
from app.services.telegram_service import send_telegram_booking_request
from app.logger import logger

from app.config import (
    MAX_RETRIES,
    RETRY_DELAY_SECONDS,
    STATUS_CONTACTING_RESTAURANT,
    STATUS_CONFIRMED,
    STATUS_REJECTED,
    STATUS_FAILED_NO_RESPONSE,
)


def send_to_restaurant(state: BookingState):
    booking = state.booking
    restaurant = state.selected_restaurant

    booking_id = state.booking_id or f"BK{random.randint(1000, 9999)}"

    logger.info("Sending booking request to restaurant via Telegram")

    save_booking(
        booking_id,
        booking,
        restaurant,
        STATUS_CONTACTING_RESTAURANT,
    )

    send_telegram_booking_request(
        booking_id=booking_id,
        booking=booking,
        restaurant=restaurant,
    )

    print("\n✅ Telegram booking request sent.")
    print("Waiting for restaurant response from Telegram...\n")

    attempts = 0

    while attempts < MAX_RETRIES:
        status = get_booking_status(booking_id)

        if status == STATUS_CONFIRMED:
            confirmation_message = booking_confirmed_message(
                booking_id=booking_id,
                booking=booking,
                restaurant=restaurant,
            )

            send_email(
                to_email=booking.email,
                subject=f"Booking Confirmed - {restaurant.name} - {booking_id}",
                body=confirmation_message,
            )

            return {
                "booking_id": booking_id,
                "booking_status": STATUS_CONFIRMED,
                "messages": [
                    AIMessage(content=confirmation_message)
                ],
            }

        if status == STATUS_REJECTED:
            rejection_message = booking_rejected_message(
                booking_id=booking_id,
                booking=booking,
                restaurant=restaurant,
            )

            return {
                "booking_id": booking_id,
                "booking_status": STATUS_REJECTED,
                "messages": [
                    AIMessage(content=rejection_message)
                ],
            }

        if status == "hold":
            print("⏳ Restaurant placed booking on HOLD.")
            print(f"Checking again in {RETRY_DELAY_SECONDS} seconds...")
            time.sleep(RETRY_DELAY_SECONDS)
            continue

        attempts += 1

        print(
            f"No Telegram response yet "
            f"({attempts}/{MAX_RETRIES}). "
            f"Checking again in {RETRY_DELAY_SECONDS} seconds..."
        )

        time.sleep(RETRY_DELAY_SECONDS)

    failed_message = booking_failed_message(
        booking_id=booking_id,
        booking=booking,
        max_retries=MAX_RETRIES,
        restaurant=restaurant,
    )

    return {
        "booking_id": booking_id,
        "booking_status": STATUS_FAILED_NO_RESPONSE,
        "messages": [
            AIMessage(content=failed_message)
        ],
    }