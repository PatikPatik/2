from flask import Flask
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import nest_asyncio

# ✅ Токен бота
TOKEN = "8190768971:AAGGSA5g-hUnrc34R8gOwwjfSez8BJ6Puz8"

# ✅ Flask-сервер для render / pella
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Telegram bot is running"

# ✅ Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["💰 Баланс", "🚀 Купить хешрейт"],
        ["👥 Пригласить друга", "ℹ️ Помощь"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я бот для облачного майнинга.", reply_markup=reply_markup)

# ✅ Обработка текста (нажатий на кнопки)
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💰 Баланс":
        await update.message.reply_text("Ваш текущий баланс: 0.000123 BTC")

    elif text == "🚀 Купить хешрейт":
        await update.message.reply_text("Покупка хешрейта пока недоступна.")

    elif text == "👥 Пригласить друга":
        await update.message.reply_text("Ваша реферальная ссылка: https://t.me/Ne_skam777_bot?start=123")

    elif text == "ℹ️ Помощь":
        await update.message.reply_text("Я бот для облачного майнинга. Команды: /start, 💰 Баланс и другие.")

    else:
        await update.message.reply_text("Неизвестная команда. Попробуйте ещё раз.")

# ✅ Основной бот
async def telegram_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Telegram bot started")
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

# ✅ Запуск Flask и Telegram параллельно
if __name__ == "__main__":
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.create_task(telegram_bot())
    app.run(host="0.0.0.0", port=5000)
