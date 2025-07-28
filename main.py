import logging
import asyncio
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8190768971:AAGGSA5g-hUnrc34R8gOwwjfSez8BJ6Puz8"

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Flask сервер (для Render/Pella)
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

# Обработчики нажатий кнопок
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ваш текущий баланс: 0 USDT")

async def buy_hashrate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Чтобы купить хешрейт, выберите тариф на сайте.")

async def invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пригласите друга и получите 1% от его добычи.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напишите /start, чтобы вызвать меню. Если остались вопросы — обращайтесь в поддержку.")

# Запуск Telegram бота
async def telegram_bot():
    application = Application.builder().token(TOKEN).build()

    # Регистрируем команды и кнопки
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^💰 Баланс$"), balance))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🚀 Купить хешрейт$"), buy_hashrate))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^👥 Пригласить друга$"), invite))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^ℹ️ Помощь$"), help_command))

    print("✅ Telegram bot started")
    await application.run_polling()

# Запуск Flask и Telegram
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(telegram_bot())
    app.run(host="0.0.0.0", port=5000)
