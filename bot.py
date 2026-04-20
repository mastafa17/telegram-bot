import telebot
import os

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

print("BOT STARTED")

@bot.message_handler(func=lambda m: True)
def all_messages(message):
    print("GOT:", message.text)
    bot.reply_to(message, "OK")

bot.remove_webhook()

# مهم جداً: بدون أي proxy settings
bot.infinity_polling(skip_pending=True)
