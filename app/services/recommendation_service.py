import json
from pathlib import Path


DATA_PATH = Path("app/data/restaurants.json")


def load_restaurants():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def recommend_restaurants(preference, limit=10):
    restaurants = load_restaurants()
    results = []

    for restaurant in restaurants:
        score = 0

        if preference.location:
            if preference.location.lower() == restaurant["location"].lower():
                score += 2
            else:
                continue

        if preference.cuisine:
            cuisine = preference.cuisine.lower()
            if cuisine in restaurant["cuisine"]:
                score += 3

        if preference.budget:
            if preference.budget == restaurant["budget"]:
                score += 2

        if preference.min_rating:
            if restaurant["rating"] >= preference.min_rating:
                score += 2
            else:
                continue

        if preference.dietary:
            dietary = preference.dietary.lower()
            if dietary in restaurant["dietary"]:
                score += 2

        if preference.ambience:
            ambience = preference.ambience.lower()
            if ambience in restaurant["ambience"]:
                score += 1

        restaurant["score"] = score
        results.append(restaurant)

    results.sort(
        key=lambda item: (item["score"], item["rating"]),
        reverse=True
    )

    return results[:limit]