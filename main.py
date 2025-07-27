import os
from threading import Thread
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)

TOKEN = os.environ.get("BOT_TOKEN")  # или вставь напрямую

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is alive!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🛒 Купить", "👤 Профиль"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Выбери действие:", reply_markup=reply_markup)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🛒 Купить":
        await update.message.reply_text("🔄 Загружаю каталог...")
    elif text == "👤 Профиль":
        await update.message.reply_text("🧾 Вот информация о твоём профиле.")
    else:
        await update.message.reply_text("Я не понимаю эту команду 😕")

async def telegram_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    print("✅ Telegram bot started")
    await application.run_polling()

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    import asyncio
    asyncio.run(telegram_bot())
