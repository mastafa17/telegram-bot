import telebot

bot = telebot.TeleBot("YOUR_TOKEN")

@bot.message_handler(content_types=['photo', 'document', 'text'])
def handler(message):
    print("RECEIVED:", message.content_type)

    if message.content_type == "photo":
        file_id = message.photo[-1].file_id
        print("FILE ID:", file_id)
        bot.reply_to(message, file_id)
    else:
        bot.reply_to(message, message.content_type)

# مهم جداً:
bot.remove_webhook()

bot.infinity_polling()
