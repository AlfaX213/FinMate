from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
import os
from dotenv import load_dotenv

from app.services.gemini_service import parse_transaction
from app.services.sheets_service import append_transaction_row

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # ============================================
    # SINGLE TRANSACTION
    # ============================================
    if len(lines) == 1:

        try:
            transaction = parse_transaction(lines[0])
        except Exception as error:
            print("Gemini error:", error)

            await update.message.reply_text(
                "❌ Sorry, I couldn't understand that transaction."
            )
            return

        append_transaction_row({
            "type": transaction.type,
            "amount": transaction.amount,
            "category": transaction.category,
            "description": transaction.description,
        })

        emoji = "💰" if transaction.type == "income" else "💸"

        await update.message.reply_text(
            f"✅ Saved transaction\n\n"
            f"{emoji} Type: {transaction.type}\n"
            f"💵 Amount: Rp{transaction.amount:,}\n"
            f"📂 Category: {transaction.category}\n"
            f"📝 Description: {transaction.description}"
        )
        return

    # ============================================
    # MULTIPLE TRANSACTIONS
    # ============================================

    saved = []

    for line in lines:

        try:
            transaction = parse_transaction(line)
        except Exception as error:
            print(f"Gemini error for '{line}':", error)
            continue

        append_transaction_row({
            "type": transaction.type,
            "amount": transaction.amount,
            "category": transaction.category,
            "description": transaction.description,
        })

        saved.append(transaction)

    if not saved:
        await update.message.reply_text(
            "❌ No valid transactions found."
        )
        return

    reply = f"✅ Saved {len(saved)} transaction(s)\n\n"

    for transaction in saved:

        emoji = "💰" if transaction.type == "income" else "💸"

        reply += (
            f"{emoji} {transaction.description}\n"
            f"Rp{transaction.amount:,} • {transaction.category}\n\n"
        )

    await update.message.reply_text(reply)


app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_message
    )
)

print("FinMate bot started...")

app.run_polling()