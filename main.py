from Venue_booking_agent.app.runner import run_agent
from Venue_booking_agent.app.services.storage_service import init_db

if __name__ == "__main__":
    init_db()
    run_agent()