import asyncio
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
import nest_asyncio

nest_asyncio.apply()

TOKEN = '8190768971:AAGGSA5g-hUnrc34R8gOwwjfSez8BJ6Puz8'

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Bot is running'

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("💰 Баланс", callback_data='balance'),
         InlineKeyboardButton("🚀 Купить хешрейт", callback_data='buy')],
        [InlineKeyboardButton("👥 Пригласить друга", callback_data='invite'),
         InlineKeyboardButton("ℹ️ Помощь", callback_data='help')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для облачного майнинга.",
                                    reply_markup=get_main_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'balance':
        await query.edit_message_text("💰 Ваш баланс: 0.00 USDT")
    elif query.data == 'buy':
        await query.edit_message_text("🚀 Купить хешрейт: Пока недоступно.")
    elif query.data == 'invite':
        await query.edit_message_text("👥 Пригласить друга: отправьте ему вашу ссылку.")
    elif query.data == 'help':
        await query.edit_message_text("ℹ️ Помощь: Напишите @youradmin.")

async def telegram_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Telegram bot started")
    await application.run_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(telegram_bot())
    app.run(host="0.0.0.0", port=5000)
