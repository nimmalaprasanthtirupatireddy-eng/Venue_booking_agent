import sqlite3
from pathlib import Path

DB_PATH = Path("bookings.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        booking_id TEXT UNIQUE,

        customer_name TEXT,
        customer_phone TEXT,
        customer_email TEXT,

        restaurant_id TEXT,
        restaurant_name TEXT,
        restaurant_phone TEXT,

        booking_date TEXT,
        booking_time TEXT,
        party_size INTEGER,
        dietary TEXT,

        status TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_booking(
    booking_id,
    booking,
    restaurant,
    status,
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO bookings (
        booking_id,

        customer_name,
        customer_phone,
        customer_email,

        restaurant_id,
        restaurant_name,
        restaurant_phone,

        booking_date,
        booking_time,
        party_size,
        dietary,

        status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        booking_id,

        booking.name,
        booking.phone_number,
        booking.email,

        restaurant.id,
        restaurant.name,
        restaurant.phone,

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

        customer_name,
        customer_phone,
        customer_email,

        restaurant_id,
        restaurant_name,
        restaurant_phone,

        booking_date,
        booking_time,
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

            "customer_name": row[1],
            "customer_phone": row[2],
            "customer_email": row[3],

            "restaurant_id": row[4],
            "restaurant_name": row[5],
            "restaurant_phone": row[6],

            "date": row[7],
            "time": row[8],
            "party_size": row[9],
            "dietary": row[10],

            "status": row[11],
            "created_at": row[12],
        }
        for row in rows
    ]


def get_booking_by_id(booking_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        booking_id,

        customer_name,
        customer_phone,
        customer_email,

        restaurant_id,
        restaurant_name,
        restaurant_phone,

        booking_date,
        booking_time,
        party_size,
        dietary,

        status,
        created_at
    FROM bookings
    WHERE booking_id = ?
    """, (booking_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "booking_id": row[0],

        "customer_name": row[1],
        "customer_phone": row[2],
        "customer_email": row[3],

        "restaurant_id": row[4],
        "restaurant_name": row[5],
        "restaurant_phone": row[6],

        "date": row[7],
        "time": row[8],
        "party_size": row[9],
        "dietary": row[10],

        "status": row[11],
        "created_at": row[12],
    }