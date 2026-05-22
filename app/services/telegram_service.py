import os
import asyncio

from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError, TimedOut

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_RESTAURANT_CHAT_ID = os.getenv("TELEGRAM_RESTAURANT_CHAT_ID")


def build_booking_message(booking_id, booking, restaurant):
    return f"""
📌 New Booking Request

Booking ID: {booking_id}

Restaurant: {restaurant.name}
Restaurant Phone: {restaurant.phone}

Customer: {booking.name}
Customer Phone: {booking.phone_number}
Customer Email: {booking.email}

Date: {booking.date}
Time: {booking.time}
Guests: {booking.party_size}
Dietary: {booking.dietary}

Please choose:
✅ ACCEPT
❌ REJECT
⏳ HOLD
"""


async def send_telegram_booking_async(booking_id, booking, restaurant):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    keyboard = [
        [
            InlineKeyboardButton("✅ ACCEPT", callback_data=f"accept:{booking_id}"),
            InlineKeyboardButton("❌ REJECT", callback_data=f"reject:{booking_id}"),
            InlineKeyboardButton("⏳ HOLD", callback_data=f"hold:{booking_id}"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await bot.send_message(
        chat_id=TELEGRAM_RESTAURANT_CHAT_ID,
        text=build_booking_message(booking_id, booking, restaurant),
        reply_markup=reply_markup,
        read_timeout=30,
        write_timeout=30,
        connect_timeout=30,
        pool_timeout=30,
    )


def send_telegram_booking_request(booking_id, booking, restaurant):
    try:
        asyncio.run(
            send_telegram_booking_async(
                booking_id,
                booking,
                restaurant,
            )
        )

        print("✅ Telegram booking request sent.")
        return True

    except TimedOut:
        print("⚠️ Telegram timeout occurred, but message may still be delivered.")
        return False

    except TelegramError as e:
        print(f"❌ Telegram error: {e}")
        return False

    except Exception as e:
        print(f"❌ General Telegram error: {e}")
        return False