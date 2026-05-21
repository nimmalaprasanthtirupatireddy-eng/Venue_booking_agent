from Venue_booking_agent.app.config import VALID_RESTAURANT_RESPONSES


def get_restaurant_response():
    print("\nRestaurant Options:")
    print("1. accept")
    print("2. reject")
    print("3. hold")
    print("4. no_response")

    response = input("\nRestaurant reply: ").strip().lower()

    if response not in VALID_RESTAURANT_RESPONSES:
        return "no_response"

    return response