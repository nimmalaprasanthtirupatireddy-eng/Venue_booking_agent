QUESTIONS = [
    ("name", "What is your name?"),
    ("phone_number", "What is your phone number?"),
    ("email", "What is your email address?"),
    ("date", "What date would you like to reserve? (DD/MM/YYYY)"),
    ("time", "What time would you prefer?"),
    ("party_size", "How many guests will be joining?"),
    ("dietary", "Any dietary requirements? (Type 'none' if no preferences)"),
]


def get_missing_field(booking):
    for field, question in QUESTIONS:
        if getattr(booking, field) is None:
            return field, question

    return None, None


def parse_input(field_name, user_input):
    user_input = user_input.strip()

    if field_name == "party_size":
        try:
            return int(user_input)
        except ValueError:
            raise ValueError("Please enter a valid number")

    return user_input