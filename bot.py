import telebot

bot = telebot.TeleBot("YOUR_TOKEN")

print("BOT STARTED")

@bot.message_handler(content_types=['photo'])
def get_file_id(message):
    print("PHOTO RECEIVED")

    file_id = message.photo[-1].file_id
    print("FILE ID:", file_id)

    bot.reply_to(message, file_id)

bot.remove_webhook()
bot.infinity_polling(skip_pending=True)
