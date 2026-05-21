from langchain_core.messages import HumanMessage, AIMessage

from app.models import BookingState
from app.models_recommendation import RestaurantPreference, SelectedRestaurant
from app.services.recommendation_service import recommend_restaurants


PREFERENCE_QUESTIONS = [
    ("location", "Which location/city are you in? Example: Doha"),
    ("cuisine", "What food do you prefer? Example: Indian, Arabic, Seafood, Vegan"),
    ("budget", "What is your budget? Choose $, $$, or $$$"),
    ("min_rating", "Minimum rating? Example: 4.0 or 4.5"),
    ("dietary", "Any dietary preference? Example: veg, vegan, halal, none"),
    ("ambience", "What ambience do you prefer? Example: family, romantic, fine dining, casual"),
]


def get_missing_preference(preference: RestaurantPreference):
    for field, question in PREFERENCE_QUESTIONS:
        if getattr(preference, field) is None:
            return field, question

    return None, None


def parse_preference(field, value):
    value = value.strip()

    if field == "min_rating":
        return float(value)

    if field == "dietary" and value.lower() in ["none", "no", "nothing", "na"]:
        return "none"

    return value.lower()


def format_restaurants(restaurants):
    text = "\nTop Restaurant Suggestions\n\n"

    for index, r in enumerate(restaurants, start=1):
        text += f"""
{index}. {r["name"]}
   Location : {r["location"]}
   Cuisine  : {", ".join(r["cuisine"])}
   Budget   : {r["budget"]}
   Rating   : {r["rating"]}
   Dietary  : {", ".join(r["dietary"])}
   Ambience : {", ".join(r["ambience"])}
"""

    text += "\nPlease choose restaurant number 1-10."

    return text


def recommend_restaurant_node(state: BookingState):
    last_user_message = None

    for msg in reversed(state.messages):
        if isinstance(msg, HumanMessage):
            last_user_message = msg.content.strip()
            break

    preference_data = state.restaurant_preference.model_dump()

    missing_field, question = get_missing_preference(state.restaurant_preference)

    if not last_user_message:
        return {
            "messages": [
                AIMessage(content="Which location/city are you in? Example: Doha")
            ]
        }

    if missing_field:
        try:
            preference_data[missing_field] = parse_preference(
                missing_field,
                last_user_message
            )
        except Exception:
            return {
                "messages": [
                    AIMessage(content=f"Invalid value. {question}")
                ]
            }

    updated_preference = RestaurantPreference(**preference_data)

    next_field, next_question = get_missing_preference(updated_preference)

    if next_question:
        return {
            "restaurant_preference": updated_preference,
            "messages": [
                AIMessage(content=next_question)
            ]
        }

    restaurants = recommend_restaurants(updated_preference)

    if not restaurants:
        return {
            "restaurant_preference": updated_preference,
            "messages": [
                AIMessage(content="No restaurants found. Please try different preferences.")
            ]
        }

    return {
        "restaurant_preference": updated_preference,
        "restaurants_recommended": True,
        "messages": [
            AIMessage(content=format_restaurants(restaurants))
        ]
    }


def choose_restaurant_node(state: BookingState):
    last_user_message = ""

    for msg in reversed(state.messages):
        if isinstance(msg, HumanMessage):
            last_user_message = msg.content.strip()
            break

    restaurants = recommend_restaurants(state.restaurant_preference)

    try:
        choice = int(last_user_message)
        selected = restaurants[choice - 1]
    except Exception:
        return {
            "messages": [
                AIMessage(content="Please choose a valid restaurant number.")
            ]
        }

    selected_restaurant = SelectedRestaurant(
        id=selected["id"],
        name=selected["name"],
        phone=selected["phone"],
    )

    return {
        "selected_restaurant": selected_restaurant,
        "restaurant_selected": True,
        "messages": [
            AIMessage(
                content=(
                    f"You selected {selected['name']}.\n\n"
                    "Now let's continue booking.\n"
                    "What is your name?"
                )
            )
        ]
    }