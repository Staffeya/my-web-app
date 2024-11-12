from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackContext

async def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("Открыть Web App", web_app=WebAppInfo(url="https://ваш-домен.com"))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать! Нажмите на кнопку для регистрации:", reply_markup=reply_markup)

def main():
    application = Application.builder().token("7652159161:AAE9-ubBxk5diNfOPABEvUJZxRa-Zysq_kg").build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()