restaurant_responses = {}


def set_restaurant_response(booking_id, response):
    restaurant_responses[booking_id] = response


def get_restaurant_response_by_booking_id(booking_id):
    return restaurant_responses.get(booking_id)