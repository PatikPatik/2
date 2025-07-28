import logging
import asyncio
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import nest_asyncio

nest_asyncio.apply()

TOKEN = "8190768971:AAGGSA5g-hUnrc34R8gOwwjfSez8BJ6Puz8"
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Telegram bot is running"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Баланс", callback_data="balance")],
        [InlineKeyboardButton("🚀 Купить хешрейт", callback_data="buy")],
        [InlineKeyboardButton("👥 Пригласить друга", callback_data="invite")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я бот для облачного майнинга.", reply_markup=reply_markup)

# Обработка inline-кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    print(f"[INLINE] Нажата кнопка: {query.data}")

    if query.data == "balance":
        await query.edit_message_text("💰 Ваш баланс: 0.00000001 BTC")
    elif query.data == "buy":
        await query.edit_message_text("🚀 Выберите тариф для покупки хешрейта.")
    elif query.data == "invite":
        await query.edit_message_text("👥 Приглашайте друзей и получайте бонусы!")
    elif query.data == "help":
        await query.edit_message_text("ℹ️ Напишите нам, если возникли вопросы.")

async def telegram_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Telegram bot started")
    await application.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(telegram_bot())
    app.run(host="0.0.0.0", port=5000)
