import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ContextTypes,
)

from app.config import (
    STATUS_CONFIRMED,
    STATUS_REJECTED,
)

from app.services.storage_service import (
    init_db,
    update_booking_status,
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def handle_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    await query.answer()

    response, booking_id = query.data.split(":")

    if response == "accept":
        status = STATUS_CONFIRMED
        message = f"✅ Booking {booking_id} accepted."

    elif response == "reject":
        status = STATUS_REJECTED
        message = f"❌ Booking {booking_id} rejected."

    elif response == "hold":
        status = "hold"
        message = f"⏳ Booking {booking_id} placed on hold."

    else:
        message = "Invalid response."
        await query.edit_message_text(text=message)
        return

    update_booking_status(
        booking_id=booking_id,
        status=status,
    )

    await query.edit_message_text(
        text=message
    )

    print("=" * 50)
    print("Restaurant Response Received")
    print("Booking ID:", booking_id)
    print("Response:", response)
    print("Saved Status:", status)
    print("=" * 50)


def main():
    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        CallbackQueryHandler(handle_button)
    )

    print("Telegram bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()