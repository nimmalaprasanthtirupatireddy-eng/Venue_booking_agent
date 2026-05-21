import re
from datetime import datetime


def clean_phone_number(value: str) -> str:
    digits = "".join(filter(str.isdigit, value))

    if len(digits) < 10:
        raise ValueError("Phone number must contain at least 10 digits")

    return digits


def validate_future_date(value: str) -> str:
    try:
        booking_date = datetime.strptime(value, "%d/%m/%Y")
    except ValueError:
        raise ValueError("Date must be in DD/MM/YYYY format")

    if booking_date.date() <= datetime.now().date():
        raise ValueError("Reservation date must be in the future")

    return value


def validate_time(value: str) -> str:
    value = value.strip()

    patterns = [
        r"^\d{1,2}:\d{2}$",
        r"^\d{1,2}\s?(am|pm|AM|PM)$",
        r"^\d{1,2}:\d{2}\s?(am|pm|AM|PM)$",
    ]

    if not any(re.match(pattern, value) for pattern in patterns):
        raise ValueError("Time must be like 09:00, 9 AM, or 09:00 PM")

    return value


def validate_party_size(value: int) -> int:
    if value <= 0:
        raise ValueError("Party size must be greater than 0")

    if value > 20:
        raise ValueError("For more than 20 guests, please call the restaurant directly")

    return value


def normalize_dietary(value: str) -> str:
    value = value.strip().lower()

    no_preference_words = [
        "none",
        "no",
        "nothing",
        "no preference",
        "no preferences",
        "na",
        "n/a",
    ]

    if value in no_preference_words:
        return "none"

    return value