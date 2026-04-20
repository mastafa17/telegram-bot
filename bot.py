import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)أول شي تعريف البوت

bot.remove_webhook()  # 👈 بعدها مباشرة

@bot.message_handler(content_types=['photo', 'document', 'text'])
def handler(message):
    print("RECEIVED:", message.content_type)

    if message.content_type == "photo":
        file_id = message.photo[-1].file_id
        print("FILE ID:", file_id)
        bot.reply_to(message, file_id)
    else:
        bot.reply_to(message, message.content_type)

bot.infinity_polling()  # 👈 تشغيل البوت
