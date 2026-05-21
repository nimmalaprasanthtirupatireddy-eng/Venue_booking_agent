import sqlite3
from pathlib import Path

DB_PATH = Path("bookings.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id TEXT,
        name TEXT,
        phone_number TEXT,
        date TEXT,
        time TEXT,
        party_size INTEGER,
        dietary TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_booking(booking_id, booking, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO bookings (
        booking_id,
        name,
        phone_number,
        date,
        time,
        party_size,
        dietary,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        booking_id,
        booking.name,
        booking.phone_number,
        booking.date,
        booking.time,
        booking.party_size,
        booking.dietary,
        status,
    ))

    conn.commit()
    conn.close()

def get_all_bookings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        booking_id,
        name,
        phone_number,
        date,
        time,
        party_size,
        dietary,
        status,
        created_at
    FROM bookings
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "booking_id": row[0],
            "name": row[1],
            "phone_number": row[2],
            "date": row[3],
            "time": row[4],
            "party_size": row[5],
            "dietary": row[6],
            "status": row[7],
            "created_at": row[8],
        }
        for row in rows
    ]