import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

print("BOT IS RUNNING")
print("BOT INFO:", bot.get_me())

bot.delete_webhook()

@bot.message_handler(func=lambda m: True)
def all_messages(message):
    print("🔥 GOT MESSAGE:", message.text)
    bot.reply_to(message, "OK")

bot.infinity_polling()
