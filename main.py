import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)
import nest_asyncio
import requests

nest_asyncio.apply()

TOKEN = os.environ.get("BOT_TOKEN") or "ТОКЕН_ОТСЮДА_ИЛИ_ОТ_ТЕБЯ"

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is alive!"

# Кнопки
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("💰 Баланс", callback_data='balance'),
     InlineKeyboardButton("🚀 Купить хешрейт", callback_data='buy')],
    [InlineKeyboardButton("👥 Пригласить друга", callback_data='refer')],
    [InlineKeyboardButton("ℹ️ Помощь", callback_data='help')]
])

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для облачного майнинга.",
        reply_markup=keyboard
    )

# Обработка кнопок
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'balance':
        await query.edit_message_text("Ваш баланс: 0.001 BTC")
    elif query.data == 'buy':
        await query.edit_message_text("Хешрейт успешно куплен! 🚀")
    elif query.data == 'refer':
        await query.edit_message_text("Пригласите друга и получите бонус! 👥")
    elif query.data == 'help':
        await query.edit_message_text("Напишите @admin для помощи.")

# Телеграм-бот
async def telegram_bot():
    requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))

    print("✅ Telegram bot started")
    await application.run_polling()

# Flask-сервер
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    asyncio.get_event_loop().run_until_complete(telegram_bot())
