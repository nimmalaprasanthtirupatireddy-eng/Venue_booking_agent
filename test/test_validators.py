import pytest

from Venue_booking_agent.app.utils.validators import (
    clean_phone_number,
    validate_future_date,
    validate_time,
    validate_party_size,
    normalize_dietary,
)


def test_clean_phone_number_valid():
    assert clean_phone_number("9447860966") == "9447860966"


def test_clean_phone_number_invalid():
    with pytest.raises(ValueError):
        clean_phone_number("12345")


def test_future_date_valid():
    assert validate_future_date("25/12/2026") == "25/12/2026"


def test_future_date_invalid_format():
    with pytest.raises(ValueError):
        validate_future_date("2026-12-25")


def test_time_valid():
    assert validate_time("09:00") == "09:00"
    assert validate_time("9 AM") == "9 AM"


def test_time_invalid():
    with pytest.raises(ValueError):
        validate_time("morning")


def test_party_size_valid():
    assert validate_party_size(4) == 4


def test_party_size_zero_invalid():
    with pytest.raises(ValueError):
        validate_party_size(0)


def test_dietary_none():
    assert normalize_dietary("no preference") == "none"