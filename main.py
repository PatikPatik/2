import asyncio
import nest_asyncio
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes
)

TOKEN = "8190768971:AAGGSA5g-hUnrc34R8gOwwjfSez8BJ6Puz8"

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Telegram bot is running!"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["💰 Баланс", "🚀 Купить хешрейт"],
        ["👥 Пригласить друга", "ℹ️ Помощь"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я бот для облачного майнинга.", reply_markup=reply_markup)

# Обработка кнопки 💰 Баланс
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 Ваш баланс: 0.00000001 BTC")

# Обработка кнопки 🚀 Купить хешрейт
async def buy_hashrate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Выберите тариф для покупки хешрейта.")

# Обработка кнопки 👥 Пригласить друга
async def invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👥 Приглашайте друзей и получайте бонусы!")

# Обработка кнопки ℹ️ Помощь
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ Напишите нам, если возникли вопросы.")

# Лог всех входящих сообщений (для отладки)
async def log_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[LOG] Получено сообщение: {update.message.text}")

# Запуск бота
async def telegram_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("^💰 Баланс$"), balance))
    application.add_handler(MessageHandler(filters.Regex("^🚀 Купить хешрейт$"), buy_hashrate))
    application.add_handler(MessageHandler(filters.Regex("^👥 Пригласить друга$"), invite))
    application.add_handler(MessageHandler(filters.Regex("^ℹ️ Помощь$"), help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_all_messages))

    print("✅ Telegram bot started")
    await application.run_polling()

# Основной запуск
if __name__ == "__main__":
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.create_task(telegram_bot())
    app.run(host="0.0.0.0", port=5000)
