from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio
import os

TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is alive!"

# Кнопки
keyboard = [
    ["💰 Баланс", "🚀 Купить хешрейт"],
    ["👥 Пригласить друга", "ℹ️ Помощь"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для облачного майнинга.",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💰 Баланс":
        await update.message.reply_text("❤️ Ваш баланс: 0.00 USDT")
    elif text == "🚀 Купить хешрейт":
        await update.message.reply_text("Вы можете купить хешрейт здесь.")
    elif text == "👥 Пригласить друга":
        await update.message.reply_text("Вот ваша реферальная ссылка: https://t.me/your_bot?start=ref123")
    elif text == "ℹ️ Помощь":
        await update.message.reply_text("Напишите нам, если возникнут вопросы.")
    else:
        await update.message.reply_text("Неизвестная команда. Используй кнопки ниже.")

async def telegram_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Telegram bot started")
    await application.run_polling()

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    asyncio.run(telegram_bot())
