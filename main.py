import logging
import nest_asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Токен твоего бота
TOKEN = "8190768971:AAGGSA5g-hUnrc34R8gOwwjfSez8BJ6Puz8"

# Настройка логов
logging.basicConfig(level=logging.INFO)
nest_asyncio.apply()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Баланс", callback_data="balance")],
        [InlineKeyboardButton("🚀 Купить хешрейт", callback_data="buy")],
        [InlineKeyboardButton("👥 Пригласить друга", callback_data="invite")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я бот для облачного майнинга.", reply_markup=reply_markup)

# Обработка нажатий на кнопки
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "balance":
        await query.edit_message_text("💰 Ваш баланс: 0.0000 BTC")
    elif query.data == "buy":
        await query.edit_message_text("🚀 Функция покупки хешрейта скоро будет доступна.")
    elif query.data == "invite":
        await query.edit_message_text("👥 Пригласите друга по ссылке и получите 1% от его добычи!")
    elif query.data == "help":
        await query.edit_message_text("ℹ️ По всем вопросам пишите: @YourSupportUsername")

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("✅ Telegram bot started")
    app.run_polling()
