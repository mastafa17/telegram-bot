import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")  # أفضل من كتابته مباشرة

bot = telebot.TeleBot(TOKEN)

print("🔥 BOT STARTED")

@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    print("📸 PHOTO RECEIVED")

    file_id = message.photo[-1].file_id
    print("FILE ID:", file_id)

    bot.reply_to(message, file_id)

bot.remove_webhook()

print("🚀 STARTING POLLING")

bot.infinity_polling(skip_pending=True)
