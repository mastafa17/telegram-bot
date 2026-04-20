import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

print("BOT STARTED")

@bot.message_handler(func=lambda m: True)
def all_messages(message):
    print("MESSAGE RECEIVED:", message.content_type)
    bot.reply_to(message, "OK")

bot.remove_webhook()

print("STARTING POLLING")

bot.infinity_polling(skip_pending=True)
