# def booking_confirmed_message(booking_id, booking):
#     return f"""
# 🎉 BOOKING CONFIRMED 🎉

# Booking ID : {booking_id}

# Customer Details
# ----------------
# Name  : {booking.name}
# Phone : {booking.phone_number}

# Reservation Details
# -------------------
# Date   : {booking.date}
# Time   : {booking.time}
# Guests : {booking.party_size}

# Dietary Requirements
# --------------------
# {booking.dietary}

# Status : CONFIRMED

# Confirmation sent to user.
# """


# def booking_rejected_message(booking_id, booking):
#     return f"""
# ❌ BOOKING REJECTED

# Booking ID : {booking_id}

# The restaurant rejected your booking request.

# Requested Details
# -----------------
# Name    : {booking.name}
# Phone   : {booking.phone_number}
# Date    : {booking.date}
# Time    : {booking.time}
# Guests  : {booking.party_size}
# Dietary : {booking.dietary}

# Please try another time slot.
# """


# def booking_failed_message(booking_id, booking, max_retries):
#     return f"""
# ❌ BOOKING FAILED

# Booking ID : {booking_id}

# No response from restaurant after {max_retries} attempts.

# Requested Reservation
# ---------------------
# Name    : {booking.name}
# Phone   : {booking.phone_number}
# Date    : {booking.date}
# Time    : {booking.time}
# Guests  : {booking.party_size}
# Dietary : {booking.dietary}

# Please try again later.
# """

def get_restaurant_name(restaurant):
    if restaurant and restaurant.name:
        return restaurant.name

    return "Selected Restaurant"


def get_restaurant_phone(restaurant):
    if restaurant and restaurant.phone:
        return restaurant.phone

    return "N/A"


def booking_confirmed_message(booking_id, booking, restaurant=None):
    restaurant_name = get_restaurant_name(restaurant)
    restaurant_phone = get_restaurant_phone(restaurant)

    return f"""
🎉 BOOKING CONFIRMED 🎉

Booking ID : {booking_id}

Restaurant Details
------------------
Restaurant : {restaurant_name}
Phone      : {restaurant_phone}

Customer Details
----------------
Name  : {booking.name}
Phone : {booking.phone_number}
Email : {booking.email}

Reservation Details
-------------------
Date   : {booking.date}
Time   : {booking.time}
Guests : {booking.party_size}

Dietary Requirements
--------------------
{booking.dietary}

Status : CONFIRMED

Confirmation sent to user.
"""


def booking_rejected_message(booking_id, booking, restaurant=None):
    restaurant_name = get_restaurant_name(restaurant)
    restaurant_phone = get_restaurant_phone(restaurant)

    return f"""
❌ BOOKING REJECTED

Booking ID : {booking_id}

Restaurant Details
------------------
Restaurant : {restaurant_name}
Phone      : {restaurant_phone}

The restaurant rejected your booking request.

Requested Details
-----------------
Name    : {booking.name}
Phone   : {booking.phone_number}
Email   : {booking.email}
Date    : {booking.date}
Time    : {booking.time}
Guests  : {booking.party_size}
Dietary : {booking.dietary}

Please try another time slot.
"""


def booking_failed_message(booking_id, booking, max_retries, restaurant=None):
    restaurant_name = get_restaurant_name(restaurant)
    restaurant_phone = get_restaurant_phone(restaurant)

    return f"""
❌ BOOKING FAILED

Booking ID : {booking_id}

Restaurant Details
------------------
Restaurant : {restaurant_name}
Phone      : {restaurant_phone}

No response from restaurant after {max_retries} attempts.

Requested Reservation
---------------------
Name    : {booking.name}
Phone   : {booking.phone_number}
Email   : {booking.email}
Date    : {booking.date}
Time    : {booking.time}
Guests  : {booking.party_size}
Dietary : {booking.dietary}

Please try again later.
"""