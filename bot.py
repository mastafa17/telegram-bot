import telebot
import os

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

print("BOT IS RUNNING")

updates = bot.get_updates()
print("UPDATES TEST:", updates)

@bot.message_handler(func=lambda m: True)
def test(message):
    print("🔥 GOT MESSAGE")
    bot.reply_to(message, "OK")

bot.infinity_polling()
