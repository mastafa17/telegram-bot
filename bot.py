import telebot

TOKEN = "8559357103:AAGTeH5u4DiwDYZDBSDn4z1O7P3pBXwDse4"
bot = telebot.TeleBot(TOKEN)

print("BOT STARTED")

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    print("PHOTO RECEIVED")

    if not message.photo:
        print("NO PHOTO OBJECT")
        return

    file_id = message.photo[-1].file_id
    print("FILE ID:", file_id)

    bot.reply_to(message, file_id)

bot.remove_webhook()
bot.infinity_polling()
