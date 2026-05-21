from langchain_core.messages import HumanMessage, AIMessage

from app.models import BookingState
from app.config import (
    STATUS_CONTACTING_RESTAURANT,
    STATUS_CANCELLED_BY_USER,
)

def consent_gate(state: BookingState):
    last_user_message = ""

    for msg in reversed(state.messages):
        if isinstance(msg, HumanMessage):
            last_user_message = msg.content.lower().strip()
            break

    if last_user_message == "yes":
        return {
            "user_consented": True,
            "booking_status": STATUS_CONTACTING_RESTAURANT
        }

    if last_user_message == "no":
        return {
            "booking_status": STATUS_CANCELLED_BY_USER
        }

    return {
        "messages": [
            AIMessage(content="Please reply ONLY with YES or NO.")
        ]
    }


def confirm_booking(state: BookingState):
    booking = state.booking

    return {
        "messages": [
            AIMessage(
                content=(
                    f"Booking request sent for {booking.name}. "
                    f"Waiting for restaurant response..."
                )
            )
        ]
    }