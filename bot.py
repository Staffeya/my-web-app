from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import json
from database import init_db, save_user_data  # Импортируем функции из database.py

# Инициализация базы данных при запуске бота
init_db()

BOT_TOKEN = "7652159161:AAE9-ubBxk5diNfOPABEvUJZxRa-Zysq_kg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создание кнопки для открытия WebApp
    keyboard = [
        [InlineKeyboardButton("Open Registration Form", web_app=WebAppInfo(url="https://ichoyou.netlify.app/"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click the button below to open the WebApp:", reply_markup=reply_markup)

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = update.effective_message.web_app_data.data
        user_data = json.loads(data)

        # Сохранение данных в базу данных
        save_user_data(user_data)

        # Пример обработки данных
        name = user_data.get('name', 'Unknown')
        age = user_data.get('age', 'Unknown')
        gender = user_data.get('gender', 'Unknown')
        interests = user_data.get('interests', 'No interests specified')
        about = user_data.get('about', 'No details provided')

        # Ответ пользователю с подтверждением
        await update.message.reply_text(
            f"Registration completed!\n\n"
            f"Name: {name}\n"
            f"Age: {age}\n"
            f"Gender: {gender}\n"
            f"Interests: {interests}\n"
            f"About: {about}"
        )

    except (json.JSONDecodeError, KeyError) as e:
        await update.message.reply_text("An error occurred while processing your data. Please try again.")
        print(f"Error handling WebApp data: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    app.run_polling()

if __name__ == "__main__":
    main()