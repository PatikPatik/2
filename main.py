import os
import asyncio
from flask import Flask, request
from telegram import Bot
from telegram.ext import Application, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")
CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

app = Flask(__name__)

# Telegram handler
@app.route(f"/{WEBHOOK_SECRET}", methods=["POST"])
def telegram_webhook():
    data = request.json
    # Обработка апдейтов Telegram, если нужно
    return "ok"

# CryptoBot handler
@app.route("/cryptobot", methods=["POST"])
def cryptobot_webhook():
    data = request.json
    # Обработка оплаты от CryptoBot
    # Например: проверка status == "paid", invoice_id и user_id
    return "ok"

@app.route("/")
def index():
    return "Bot is alive!"

# запуск Telegram-бота
async def run_telegram():
    application = Application.builder().token(TOKEN).build()

    async def start(update, context):
        await update.message.reply_text("Привет! Я живой.")

    application.add_handler(CommandHandler("start", start))
    await application.run_polling()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    from threading import Thread
    def run_flask():
        app.run(host="0.0.0.0", port=port)

    # запускаем Flask отдельно
    Thread(target=run_flask).start()

    # запускаем Telegram-бота
    asyncio.run(run_telegram())
