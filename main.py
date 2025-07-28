import asyncio
import logging
from flask import Flask
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import nest_asyncio

# 🔧 Токен
TOKEN = '8190768971:AAGGSA5g-hUnrc34R8gOwwjfSez8BJ6Puz8'

# 🌐 Flask сервер
app = Flask(__name__)

# 📋 Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🔥 Новый start с inline кнопками загружен!")  # Проверка что именно этот код работает
    keyboard = [
        [InlineKeyboardButton("💰 Баланс", callback_data="balance")],
        [InlineKeyboardButton("🚀 Купить хешрейт", callback_data="buy")],
        [InlineKeyboardButton("👥 Пригласить друга", callback_data="invite")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я бот для облачного майнинга.", reply_markup=reply_markup)

# ⚙️ Обработка нажатия на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == "balance":
        await query.edit_message_text("Ваш текущий баланс: 0.001 BTC")
    elif data == "buy":
        await query.edit_message_text("Для покупки хешрейта перейдите на сайт ...")
    elif data == "invite":
        await query.edit_message_text("Пригласите друга и получите бонус 1% от его дохода.")
    elif data == "help":
        await query.edit_message_text("Это бот для облачного майнинга. Напишите /start, чтобы начать.")

# 🚀 Запуск бота
async def run_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Telegram bot started")
    await application.run_polling()

# 🚪 Запуск Flask и бота вместе
@app.route('/')
def index():
    return 'Bot is running!'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host='0.0.0.0', port=5000)
