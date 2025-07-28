import os
import asyncio
from flask import Flask
from threading import Thread

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Вставь сюда свой токен бота
TOKEN = os.environ.get("BOT_TOKEN", "ВСТАВЬ_СЮДА_СВОЙ_ТОКЕН")

# Flask-сервер
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is alive!"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Кнопка 1", callback_data="btn1")],
        [InlineKeyboardButton("Кнопка 2", callback_data="btn2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Нажми на кнопку:", reply_markup=reply_markup)

# Обработка нажатий
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "btn1":
        await query.edit_message_text("Вы нажали на кнопку 1")
    elif query.data == "btn2":
        await query.edit_message_text("Вы нажали на кнопку 2")

# Telegram-бот
async def telegram_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Telegram bot started")
    await application.run_polling()

# Flask run
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Запуск
if __name__ == "__main__":
    Thread(target=run_flask).start()
    asyncio.run(telegram_bot())
