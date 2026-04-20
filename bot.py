import telebot

bot = telebot.TeleBot("8559357103:AAGTeH5u4DiwDYZDBSDn4z1O7P3pBXwDse4")

@bot.message_handler(content_types=['photo', 'document', 'text'])
def test(message):
    print("TYPE:", message.content_type)
    bot.reply_to(message, message.content_type)

bot.infinity_polling()
