from langchain_core.messages import HumanMessage

from app.models import BookingState
from app.graph import build_graph
from app.config import (
    STATUS_CONFIRMED,
    STATUS_REJECTED,
    STATUS_FAILED_NO_RESPONSE,
    STATUS_CANCELLED_BY_USER,
)


FINAL_STATUSES = [
    STATUS_CONFIRMED,
    STATUS_REJECTED,
    STATUS_FAILED_NO_RESPONSE,
    STATUS_CANCELLED_BY_USER,
]


def run_agent():
    graph = build_graph()

    state = BookingState()

    print("\n" + "=" * 50)
    print("Restaurant Discovery + Booking Agent")
    print("=" * 50)

    print("\nType 'quit' anytime to exit.\n")
    print("Agent: Which location/city are you in? Example: Doha\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            break

        result = graph.invoke({
            "messages": [
                HumanMessage(content=user_input)
            ],
            "restaurant_preference": state.restaurant_preference,
            "selected_restaurant": state.selected_restaurant,
            "restaurants_recommended": state.restaurants_recommended,
            "restaurant_selected": state.restaurant_selected,
            "booking": state.booking,
            "booking_id": state.booking_id,
            "info_complete": state.info_complete,
            "user_consented": state.user_consented,
            "booking_status": state.booking_status,
        })

        state = BookingState(**result)

        if state.messages:
            print("\nAgent:", state.messages[-1].content, "\n")

        if state.booking_status in FINAL_STATUSES:
            break

    print("\nSession Ended →", state.booking_status)