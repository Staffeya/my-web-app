from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import os

BOT_TOKEN = "7652159161:AAE9-ubBxk5diNfOPABEvUJZxRa-Zysq_kg"  # Убедитесь, что токен верный

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создание кнопки для открытия WebApp
    keyboard = [
        [InlineKeyboardButton("Open Registration Form", web_app=WebAppInfo(url="https://ichoyou.netlify.app/"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click the button below to open the WebApp:", reply_markup=reply_markup)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()