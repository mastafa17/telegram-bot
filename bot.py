import telebot

bot = telebot.TeleBot("TOKEN")

print("BOT STARTED")

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    file_id = message.photo[-1].file_id
    print(file_id)
    bot.reply_to(message, file_id)

bot.remove_webhook()
bot.infinity_polling(skip_pending=True)
