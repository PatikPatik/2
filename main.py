import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from threading import Thread

TOKEN = os.getenv("BOT_TOKEN")
CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

app = Flask(__name__)

@app.route(f"/{WEBHOOK_SECRET}", methods=["POST"])
def telegram_webhook():
    data = request.json
    return "ok"

@app.route("/cryptobot", methods=["POST"])
def cryptobot_webhook():
    data = request.json
    return "ok"

@app.route("/")
def index():
    return "Bot is alive!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я живой.")

async def telegram_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    await application.initialize()
    await application.start()
    print("✅ Telegram bot started")

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Запускаем Flask-сервер в отдельном потоке
    Thread(target=run_flask).start()

    # Получаем текущий event loop и запускаем в нём Telegram-бот
    loop = asyncio.get_event_loop()
    loop.create_task(telegram_bot())
    loop.run_forever()
