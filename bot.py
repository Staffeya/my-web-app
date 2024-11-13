from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import json
import os

# Используйте переменную окружения для токена или задайте токен напрямую
BOT_TOKEN = os.getenv("BOT_TOKEN", "7652159161:AAE9-ubBxk5diNfOPABEvUJZxRa-Zysq_kg")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Open Registration Form", web_app=WebAppInfo(url="https://ichoyou.netlify.app/"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click the button below to start the registration:", reply_markup=reply_markup)

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = update.effective_message.web_app_data.data
        user_data = json.loads(data)

        # Сохранение данных пользователя
        user_id = update.effective_user.id
        name = user_data.get('name', 'Unknown')
        age = user_data.get('age', 'Unknown')
        gender = user_data.get('gender', 'Unknown')
        city = user_data.get('city', 'Unknown')
        about = user_data.get('about', 'No details provided')

        # Ответ пользователю
        await update.message.reply_text(
            f"Thank you for registering, {name}!\n\n"
            f"Age: {age}\nGender: {gender}\nCity: {city}\nAbout: {about}"
        )

        # Логирование
        print(f"User {user_id} registered with data: {user_data}")

    except (json.JSONDecodeError, KeyError) as e:
        await update.message.reply_text("There was an error processing your registration data. Please try again.")
        print(f"Error handling webapp data for user {update.effective_user.id}: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))

    app.run_polling()

if __name__ == "__main__":
    main