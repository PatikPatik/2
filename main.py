import os
from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, ContextTypes
)
import asyncio

# Токен бота из переменной окружения
TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is alive!"

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["💰 Баланс", "🚀 Купить хешрейт"],
                ["👥 Пригласить друга", "ℹ️ Помощь"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я бот для облачного майнинга.", reply_markup=reply_markup)

# Функция запуска Telegram-бота
async def telegram_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("✅ Telegram bot started")
    await application.run_polling()

# Функция запуска Flask
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Запуск Flask-сервера в отдельном потоке
    Thread(target=run_flask).start()

    # Запуск Telegram-бота с использованием уже запущенного event loop
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(telegram_bot())
