from langchain_core.messages import AIMessage

from Venue_booking_agent.app.models import BookingState


def cancel_booking(state: BookingState):
    return {
        "booking_status": "cancelled",
        "messages": [
            AIMessage(content="Booking cancelled.")
        ]
    }