import os
import asyncio
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import nest_asyncio

TOKEN = os.getenv("BOT_TOKEN")  # Убедись, что переменная окружения настроена на Render

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Bot is alive!"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Проверить баланс", callback_data="balance")],
        [InlineKeyboardButton("📈 Статистика", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Что ты хочешь сделать?", reply_markup=reply_markup)

# Обработка кнопок
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "balance":
        await query.edit_message_text(text="💰 Ваш баланс: 0.000123 BTC")
    elif query.data == "stats":
        await query.edit_message_text(text="📈 Статистика: хешрейт 12 GH/s")

# Telegram бот
async def telegram_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_button))
    await application.initialize()
    await application.start()
    print("✅ Telegram bot started")
    await application.updater.wait_until_closed()

# Flask-сервер
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    nest_asyncio.apply()  # Разрешает повторный запуск asyncio-цикла
    Thread(target=run_flask).start()
    asyncio.get_event_loop().run_until_complete(telegram_bot())
