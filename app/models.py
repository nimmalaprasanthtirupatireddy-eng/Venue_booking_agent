from datetime import datetime
from typing import Optional, Annotated

from pydantic import BaseModel, field_validator
from langgraph.graph.message import add_messages

from app.config import STATUS_PENDING

from app.utils.validators import (
    clean_phone_number,
    validate_future_date,
    validate_time,
    validate_party_size,
    normalize_dietary,
)

class BookingDetails(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    party_size: Optional[int] = None
    dietary: Optional[str] = None

    @field_validator("date")
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return v
        return validate_future_date(v)


    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return v
        return clean_phone_number(v)


    @field_validator("time")
    @classmethod
    def validate_booking_time(cls, v):
        if v is None:
            return v
        return validate_time(v)


    @field_validator("party_size")
    @classmethod
    def validate_booking_party_size(cls, v):
        if v is None:
            return v
        return validate_party_size(v)


    @field_validator("dietary")
    @classmethod
    def validate_dietary(cls, v):
        if v is None:
            return v
        return normalize_dietary(v)


class BookingState(BaseModel):
    messages: Annotated[list, add_messages] = []

    booking: BookingDetails = BookingDetails()
    booking_id: Optional[str] = None
    info_complete: bool = False
    user_consented: bool = False
    booking_status: str = STATUS_PENDING