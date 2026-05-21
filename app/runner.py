from langchain_core.messages import HumanMessage

from app.models import BookingState
from app.graph import build_graph


def run_agent():
    graph = build_graph()

    state = BookingState()

    print("\n" + "=" * 50)
    print("Restaurant Booking Agent")
    print("=" * 50)

    print("\nType 'quit' anytime to exit.\n")

    print("Agent: What is your name?\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            break

        result = graph.invoke({
            "messages": [
                HumanMessage(content=user_input)
            ],
            "booking": state.booking,
            "info_complete": state.info_complete,
            "user_consented": state.user_consented,
            "booking_status": state.booking_status,
        })

        state = BookingState(**result)

        if state.messages:
            print("\nAgent:", state.messages[-1].content, "\n")

        if state.info_complete:
            confirm_input = input("You (YES/NO): ").strip()

            result = graph.invoke({
                "messages": [
                    HumanMessage(content=confirm_input)
                ],
                "booking": state.booking,
                "info_complete": state.info_complete,
                "user_consented": state.user_consented,
                "booking_status": state.booking_status,
            })

            state = BookingState(**result)

            if state.messages:
                print("\nAgent:", state.messages[-1].content, "\n")

            break

    print("\nSession Ended →", state.booking_status)