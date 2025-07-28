import logging
import asyncio
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import nest_asyncio

nest_asyncio.apply()

# 🔐 Токен бота
TOKEN = "8190768971:AAGGSA5g-hUnrc34R8gOwwjfSez8BJ6Puz8"

# 🌐 Flask-приложение
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Telegram bot is running"

# 🎮 Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["💰 Баланс", "🚀 Купить хешрейт"],
        ["👥 Пригласить друга", "ℹ️ Помощь"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я бот для облачного майнинга.", reply_markup=reply_markup)

# 🧠 Обработка ВСЕХ входящих сообщений
async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text if update.message else "Нет текста"
    print(f"[ВСЁ] Получено: {msg}")

    if msg == "💰 Баланс":
        await update.message.reply_text("💰 Ваш баланс: 0.00000001 BTC")
    elif msg == "🚀 Купить хешрейт":
        await update.message.reply_text("🚀 Выберите тариф для покупки хешрейта.")
    elif msg == "👥 Пригласить друга":
        await update.message.reply_text("👥 Приглашайте друзей и получайте бонусы!")
    elif msg == "ℹ️ Помощь":
        await update.message.reply_text("ℹ️ Напишите нам, если возникли вопросы.")

# 🚀 Запуск бота
async def telegram_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, handle_all))

    print("✅ Telegram bot started")
    await application.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(telegram_bot())
    app.run(host="0.0.0.0", port=5000)
