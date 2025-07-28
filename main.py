import asyncio
import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = "8190768971:AAGGSA5g-hUnrc34R8gOwwjfSez8BJ6Puz8"

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is alive!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("💰 Баланс", callback_data="balance"),
            InlineKeyboardButton("🚀 Купить хешрейт", callback_data="buy_hashrate")
        ],
        [
            InlineKeyboardButton("👥 Пригласить друга", callback_data="invite"),
            InlineKeyboardButton("ℹ️ Помощь", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я бот для облачного майнинга.", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "balance":
        await query.edit_message_text("💰 Ваш баланс: 0.00 USDT")
    elif data == "buy_hashrate":
        await query.edit_message_text("🚀 Чтобы купить хешрейт, перейдите по ссылке: https://example.com")
    elif data == "invite":
        await query.edit_message_text("👥 Пригласите друга и получите 1% от его дохода!")
    elif data == "help":
        await query.edit_message_text("ℹ️ Напишите /start чтобы начать заново.")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я не понял эту команду. Напишите /start.")

async def telegram_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    print("✅ Telegram bot started")
    await application.run_polling()

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    asyncio.get_event_loop().run_until_complete(telegram_bot())
