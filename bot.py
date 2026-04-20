import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

print("BOT IS RUNNING")

@bot.message_handler(func=lambda m: True)
def test(message):
    print("🔥 GOT MESSAGE")
    print("TYPE:", message.content_type)
    bot.reply_to(message, "OK")

bot.remove_webhook()
bot.infinity_polling(skip_pending=True)

print(bot.get_me())
