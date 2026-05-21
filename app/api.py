from fastapi import FastAPI
from pydantic import BaseModel

from langchain_core.messages import HumanMessage

from app.graph import build_graph
from app.models import BookingState, BookingDetails
from app.services.storage_service import init_db, get_all_bookings, save_booking
from app.services.notification_service import (
    booking_confirmed_message,
    booking_rejected_message,
    booking_failed_message,
)
from app.config import (
    MAX_RETRIES,
    STATUS_CONTACTING_RESTAURANT,
    STATUS_CONFIRMED,
    STATUS_REJECTED,
    STATUS_FAILED_NO_RESPONSE,
    BOOKING_ID_PREFIX,
)

import random


app = FastAPI(title="Restaurant Booking Agent API")

graph = build_graph()
sessions = {}


# =========================================================
# REQUEST MODELS
# =========================================================

class ChatRequest(BaseModel):
    session_id: str
    message: str


class DirectBookingRequest(BaseModel):
    name: str
    phone_number: str
    email: str
    date: str
    time: str
    party_size: int
    dietary: str = "none"
    restaurant_response: str = "accept"


# =========================================================
# STARTUP
# =========================================================

@app.on_event("startup")
def startup():
    init_db()


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# =========================================================
# GET ALL BOOKINGS
# =========================================================

@app.get("/bookings")
def bookings():
    return {
        "bookings": get_all_bookings()
    }


# =========================================================
# CHAT-BASED BOOKING API
# =========================================================

@app.post("/chat")
def chat(request: ChatRequest):
    session_id = request.session_id

    if session_id not in sessions:
        sessions[session_id] = BookingState()

    state = sessions[session_id]

    result = graph.invoke({
        "messages": [
            HumanMessage(content=request.message)
        ],
        "booking": state.booking,
        "booking_id": state.booking_id,
        "info_complete": state.info_complete,
        "user_consented": state.user_consented,
        "booking_status": state.booking_status,
    })

    new_state = BookingState(**result)
    sessions[session_id] = new_state

    response_message = ""

    if new_state.messages:
        response_message = new_state.messages[-1].content

    return {
        "session_id": session_id,
        "reply": response_message,
        "booking": new_state.booking.model_dump(),
        "booking_id": new_state.booking_id,
        "status": new_state.booking_status,
        "info_complete": new_state.info_complete,
    }


# =========================================================
# DIRECT BOOKING API
# =========================================================

@app.post("/book")
def book(request: DirectBookingRequest):
    booking = BookingDetails(
        name=request.name,
        phone_number=request.phone_number,
        email=request.email,
        date=request.date,
        time=request.time,
        party_size=request.party_size,
        dietary=request.dietary,
    )

    booking_id = f"{BOOKING_ID_PREFIX}{random.randint(1000, 9999)}"

    restaurant_response = request.restaurant_response.lower().strip()

    if restaurant_response == "accept":
        status = STATUS_CONFIRMED

        save_booking(
            booking_id,
            booking,
            status,
        )

        message = booking_confirmed_message(
            booking_id,
            booking,
        )

    elif restaurant_response == "reject":
        status = STATUS_REJECTED

        save_booking(
            booking_id,
            booking,
            status,
        )

        message = booking_rejected_message(
            booking_id,
            booking,
        )

    elif restaurant_response == "no_response":
        status = STATUS_FAILED_NO_RESPONSE

        save_booking(
            booking_id,
            booking,
            status,
        )

        message = booking_failed_message(
            booking_id,
            booking,
            MAX_RETRIES,
        )

    else:
        status = STATUS_CONTACTING_RESTAURANT

        message = "Booking request is currently on hold. Please check again later."

    return {
        "booking_id": booking_id,
        "status": status,
        "message": message,
        "booking": booking.model_dump(),
    }