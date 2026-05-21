from langgraph.graph import StateGraph, START, END

from Venue_booking_agent.app.models import BookingState
from Venue_booking_agent.app.nodes.gather_info import gather_info
from Venue_booking_agent.app.nodes.consent import consent_gate, confirm_booking
from Venue_booking_agent.app.nodes.restaurant import send_to_restaurant
from Venue_booking_agent.app.nodes.cancel import cancel_booking

from Venue_booking_agent.app.config import (
    STATUS_CONTACTING_RESTAURANT,
    STATUS_CANCELLED_BY_USER,
)

def route_after_gather(state: BookingState):
    if state.info_complete:
        return "consent_gate"

    return END


def route_after_consent(state: BookingState):
    if state.booking_status == STATUS_CONTACTING_RESTAURANT:
        return "confirm_booking"

    if state.booking_status == STATUS_CANCELLED_BY_USER:
        return "cancel_booking"

    return END


def build_graph():
    graph = StateGraph(BookingState)

    graph.add_node("gather_info", gather_info)
    graph.add_node("consent_gate", consent_gate)
    graph.add_node("confirm_booking", confirm_booking)
    graph.add_node("send_to_restaurant", send_to_restaurant)
    graph.add_node("cancel_booking", cancel_booking)

    graph.add_edge(START, "gather_info")

    graph.add_conditional_edges("gather_info", route_after_gather)
    graph.add_conditional_edges("consent_gate", route_after_consent)

    graph.add_edge("confirm_booking", "send_to_restaurant")
    graph.add_edge("send_to_restaurant", END)
    graph.add_edge("cancel_booking", END)

    return graph.compile()