import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is alive!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Купить", callback_data='buy')],
        [InlineKeyboardButton("👤 Профиль", callback_data='profile')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Выбери действие:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "buy":
        await query.edit_message_text("Вы выбрали покупку.")
    elif query.data == "profile":
        await query.edit_message_text("Это ваш профиль.")

async def telegram_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    await application.initialize()
    await application.start()
    print("✅ Telegram bot started")

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    import asyncio
    asyncio.run(telegram_bot())
