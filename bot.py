from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import json

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Open Registration Form", web_app=WebAppInfo(url="https://ichoyou.netlify.app/"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click the button below to start the registration:", reply_markup=reply_markup)

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.effective_message.web_app_data.data
    user_data = json.loads(data)

    # Сохранение данных пользователя
    user_id = update.effective_user.id
    name = user_data['name']
    age = user_data['age']
    gender = user_data['gender']
    city = user_data['city']
    about = user_data['about']

    # Вы можете сохранить данные в базу данных или обработать их здесь
    await update.message.reply_text(f"Thank you for registering, {name}!")

def main():
    app = Application.builder().token("7652159161:AAE9-ubBxk5diNfOPABEvUJZxRa-Zysq_kg").build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()