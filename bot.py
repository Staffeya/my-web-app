from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, ConversationHandler, filters
import json
import os

BOT_TOKEN = "7652159161:AAE9-ubBxk5diNfOPABEvUJZxRa-Zysq_kg"  # Убедитесь, что токен верный

# Определяем этапы регистрации
NAME, AGE, USE_WEBAPP, CITY, ABOUT = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Давайте начнем регистрацию. Как вас зовут?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Сколько вам лет?")
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['age'] = update.message.text

    # Включаем WebApp на этапе сбора дополнительной информации
    keyboard = [
        [InlineKeyboardButton("Открыть форму в WebApp", web_app=WebAppInfo(url="https://ichoyou.netlify.app/"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нажмите на кнопку ниже, чтобы продолжить регистрацию в WebApp.", reply_markup=reply_markup)
    return USE_WEBAPP

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = update.effective_message.web_app_data.data
        user_data = json.loads(data)

        # Сохранение данных, переданных из WebApp
        context.user_data['gender'] = user_data.get('gender', 'Unknown')
        context.user_data['city'] = user_data.get('city', 'Unknown')
        context.user_data['about'] = user_data.get('about', 'No details provided')

        # Переход к следующему этапу (например, подтверждение регистрации)
        await update.message.reply_text(
            f"Данные из WebApp получены!\n\n"
            f"Имя: {context.user_data['name']}\n"
            f"Возраст: {context.user_data['age']}\n"
            f"Пол: {context.user_data['gender']}\n"
            f"Город: {context.user_data['city']}\n"
            f"О себе: {context.user_data['about']}\n\n"
            f"Регистрация завершена! Спасибо!"
        )

        # Очистка данных пользователя
        context.user_data.clear()
        return ConversationHandler.END

    except (json.JSONDecodeError, KeyError) as e:
        await update.message.reply_text("Произошла ошибка при обработке данных из WebApp. Попробуйте снова.")
        print(f"Ошибка при обработке данных из WebApp: {e}")
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Регистрация отменена.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Создаем обработчик разговоров для управления этапами
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            USE_WEBAPP: [MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
