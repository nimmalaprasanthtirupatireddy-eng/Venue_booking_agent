MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 3

BOOKING_ID_PREFIX = "BK"

VALID_RESTAURANT_RESPONSES = [
    "accept",
    "reject",
    "hold",
    "no_response",
]

STATUS_PENDING = "pending"
STATUS_AWAITING_CONFIRMATION = "awaiting_user_confirmation"
STATUS_CONTACTING_RESTAURANT = "contacting_restaurant"
STATUS_CONFIRMED = "confirmed"
STATUS_REJECTED = "rejected"
STATUS_FAILED_NO_RESPONSE = "failed_no_response"
STATUS_CANCELLED_BY_USER = "cancelled_by_user"