from flask import Flask
import asyncio
import nest_asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

TOKEN = "8190768971:AAGGSA5g-hUnrc34R8gOwwjfSez8BJ6Puz8"

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Telegram bot is running"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["💰 Баланс", "🚀 Купить хешрейт"],
        ["👥 Пригласить друга", "ℹ️ Помощь"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я бот для облачного майнинга.", reply_markup=reply_markup)

# Обработка текстовых кнопок
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id
    print(f"[{chat_id}] Нажал: {text}")

    if text == "💰 Баланс":
        await update.message.reply_text("Ваш баланс: 0.001 BTC")
    elif text == "🚀 Купить хешрейт":
        await update.message.reply_text("Функция в разработке.")
    elif text == "👥 Пригласить друга":
        await update.message.reply_text("Ваша ссылка: https://t.me/Ne_skam777_bot?start=ref123")
    elif text == "ℹ️ Помощь":
        await update.message.reply_text("Команды: /start, кнопки снизу.")
    else:
        await update.message.reply_text("Не понимаю команду.")

# Основная функция запуска бота
async def run_bot():
    app_telegram = ApplicationBuilder().token(TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Telegram bot started")
    await app_telegram.initialize()
    await app_telegram.start()
    await app_telegram.updater.start_polling()
    await app_telegram.updater.idle()

if __name__ == "__main__":
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host="0.0.0.0", port=5000)
