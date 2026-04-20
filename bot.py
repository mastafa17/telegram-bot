import telebot

bot = telebot.TeleBot("8559357103:AAGTeH5u4DiwDYZDBSDn4z1O7P3pBXwDse4")

@bot.message_handler(content_types=['photo'])
def get_file_id(message):
    file_id = message.photo[-1].file_id
    print("FILE ID:", file_id)
    bot.reply_to(message, file_id)

bot.infinity_polling()
