import os
import sqlite3
import requests
from flask import Flask, request
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# === Telegram handlers ===
application = Application.builder().token(BOT_TOKEN).build()
keyboard = [[KeyboardButton("Купить 1 TH/s")]]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def create_invoice(user_id, amount=13.7, currency="USDT"):
    url = "https://pay.crypt.bot/createInvoice"
    headers = {
        "Crypto-Pay-API-Token": CRYPTOBOT_TOKEN
    }
    payload = {
        "asset": currency,
        "amount": amount,
        "description": f"Покупка 1 TH/s",
        "hidden_message": "Спасибо за оплату!",
        "payload": str(user_id),
        "allow_comments": False
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.json()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Выберите действие:", reply_markup=markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    if "купить" in text.lower():
        invoice = create_invoice(user_id)
        pay_url = invoice.get("result", {}).get("pay_url")
        if pay_url:
            await update.message.reply_text(f"💸 Оплатите по ссылке: {pay_url}")
        else:
            await update.message.reply_text("Ошибка при создании инвойса.")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route(f"/{WEBHOOK_SECRET}", methods=["POST"])
def telegram_webhook():
    update = request.get_json(force=True)
    asyncio.create_task(application.process_update(Update.de_json(update, application.bot)))
    return "ok"

@app.route("/cryptobot", methods=["POST"])
def cryptobot_webhook():
    data = request.json
    if data.get("status") == "paid":
        user_id = int(data.get("payload"))
        amount = float(data.get("amount", 0))
        purchased_ths = amount / 13.7

        conn = sqlite3.connect("mining.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = balance + ?, hashrate = hashrate + ? WHERE user_id = ?",
                       (amount, purchased_ths, user_id))

        cursor.execute("SELECT referrer_id FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if result and result[0]:
            referrer_id = result[0]
            bonus = amount * 0.01
            cursor.execute("UPDATE users SET balance = balance + ?, ref_bonus = ref_bonus + ? WHERE user_id = ?",
                           (bonus, bonus, referrer_id))

        conn.commit()
        conn.close()
    return "ok"

@app.route("/")
def index():
    return "Bot is running!"

async def run_telegram():
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

asyncio.create_task(run_telegram())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
