from langchain_core.messages import HumanMessage, AIMessage

from app.models import BookingDetails, BookingState
from app.questions import get_missing_field, parse_input
from app.config import STATUS_AWAITING_CONFIRMATION

def gather_info(state: BookingState):
    last_user_message = None

    for msg in reversed(state.messages):
        if isinstance(msg, HumanMessage):
            last_user_message = msg.content.strip()
            break

    if not last_user_message:
        return {
            "messages": [
                AIMessage(content="What is your name?")
            ]
        }

    current_booking = state.booking.model_dump()
    booking_obj = BookingDetails(**current_booking)

    missing_field, _ = get_missing_field(booking_obj)

    if not missing_field:
        return {}

    try:
        parsed_value = parse_input(missing_field, last_user_message)
        current_booking[missing_field] = parsed_value

        updated_booking = BookingDetails(**current_booking)

    except Exception as e:
        return {
            "messages": [
                AIMessage(content=f"Invalid input: {str(e)}")
            ]
        }

    _, next_question = get_missing_field(updated_booking)

    updates = {
        "booking": updated_booking
    }

    if next_question:
        updates["messages"] = [
            AIMessage(content=next_question)
        ]
    else:
        updates["info_complete"] = True
        updates["booking_status"] = STATUS_AWAITING_CONFIRMATION

        summary = f"""
Booking Summary

Name: {updated_booking.name}
Phone: {updated_booking.phone_number}
Date: {updated_booking.date}
Time: {updated_booking.time}
Guests: {updated_booking.party_size}
Dietary: {updated_booking.dietary}

Please type YES to confirm
or NO to cancel.
"""

        updates["messages"] = [
            AIMessage(content=summary)
        ]

    return updates