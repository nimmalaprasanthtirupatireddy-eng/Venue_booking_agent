from Venue_booking_agent.app.models import BookingDetails
from Venue_booking_agent.app.questions import get_missing_field, parse_input


def test_first_missing_field_is_name():
    booking = BookingDetails()
    field, question = get_missing_field(booking)

    assert field == "name"
    assert question == "What is your name?"


def test_missing_phone_after_name():
    booking = BookingDetails(name="Prasanth")
    field, question = get_missing_field(booking)

    assert field == "phone_number"


def test_parse_party_size():
    assert parse_input("party_size", "4") == 4