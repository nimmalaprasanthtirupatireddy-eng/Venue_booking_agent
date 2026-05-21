# from langgraph.graph import StateGraph, START, END

# from app.models import BookingState
# from app.nodes.recommend_restaurant import (
#     recommend_restaurant_node,
#     choose_restaurant_node,
# )
# from app.nodes.gather_info import gather_info
# from app.nodes.consent import consent_gate, confirm_booking
# from app.nodes.restaurant import send_to_restaurant
# from app.nodes.cancel import cancel_booking
# from app.config import (
#     STATUS_AWAITING_CONFIRMATION,
#     STATUS_CONTACTING_RESTAURANT,
#     STATUS_CANCELLED_BY_USER,
# )


# def route_after_recommendation(state: BookingState):
#     last_message = state.messages[-1].content if state.messages else ""

#     if "Please choose restaurant number" in last_message:
#         return "choose_restaurant"

#     return END


# def route_after_choose_restaurant(state: BookingState):
#     if state.restaurant_selected:
#         return "gather_info"

#     return END


# def route_after_gather(state: BookingState):
#     if state.booking_status == STATUS_AWAITING_CONFIRMATION:
#         return "consent_gate"

#     return END


# def route_after_consent(state: BookingState):
#     if state.booking_status == STATUS_CONTACTING_RESTAURANT:
#         return "confirm_booking"

#     if state.booking_status == STATUS_CANCELLED_BY_USER:
#         return "cancel_booking"

#     return END


# def build_graph():
#     graph = StateGraph(BookingState)

#     graph.add_node("recommend_restaurant", recommend_restaurant_node)
#     graph.add_node("choose_restaurant", choose_restaurant_node)
#     graph.add_node("gather_info", gather_info)
#     graph.add_node("consent_gate", consent_gate)
#     graph.add_node("confirm_booking", confirm_booking)
#     graph.add_node("send_to_restaurant", send_to_restaurant)
#     graph.add_node("cancel_booking", cancel_booking)

#     graph.add_edge(START, "recommend_restaurant")

#     graph.add_conditional_edges(
#         "recommend_restaurant",
#         route_after_recommendation,
#     )

#     graph.add_conditional_edges(
#         "choose_restaurant",
#         route_after_choose_restaurant,
#     )

#     graph.add_conditional_edges(
#         "gather_info",
#         route_after_gather,
#     )

#     graph.add_conditional_edges(
#         "consent_gate",
#         route_after_consent,
#     )

#     graph.add_edge("confirm_booking", "send_to_restaurant")
#     graph.add_edge("send_to_restaurant", END)
#     graph.add_edge("cancel_booking", END)

#     return graph.compile()

from langgraph.graph import StateGraph, START, END

from app.models import BookingState
from app.nodes.recommend_restaurant import (
    recommend_restaurant_node,
    choose_restaurant_node,
)
from app.nodes.gather_info import gather_info
from app.nodes.consent import consent_gate, confirm_booking
from app.nodes.restaurant import send_to_restaurant
from app.nodes.cancel import cancel_booking

from app.config import (
    STATUS_AWAITING_CONFIRMATION,
    STATUS_CONTACTING_RESTAURANT,
    STATUS_CANCELLED_BY_USER,
)


def route_from_start(state: BookingState):
    if not state.restaurants_recommended:
        return "recommend_restaurant"

    if state.restaurants_recommended and not state.restaurant_selected:
        return "choose_restaurant"

    if state.restaurant_selected and not state.info_complete:
        return "gather_info"

    if state.booking_status == STATUS_AWAITING_CONFIRMATION:
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

    graph.add_node("recommend_restaurant", recommend_restaurant_node)
    graph.add_node("choose_restaurant", choose_restaurant_node)
    graph.add_node("gather_info", gather_info)
    graph.add_node("consent_gate", consent_gate)
    graph.add_node("confirm_booking", confirm_booking)
    graph.add_node("send_to_restaurant", send_to_restaurant)
    graph.add_node("cancel_booking", cancel_booking)

    graph.add_conditional_edges(
        START,
        route_from_start,
    )

    graph.add_edge("recommend_restaurant", END)
    graph.add_edge("choose_restaurant", END)
    graph.add_edge("gather_info", END)

    graph.add_conditional_edges(
        "consent_gate",
        route_after_consent,
    )

    graph.add_edge("confirm_booking", "send_to_restaurant")
    graph.add_edge("send_to_restaurant", END)
    graph.add_edge("cancel_booking", END)

    return graph.compile()