import telebot

bot = telebot.TeleBot("YOUR_TOKEN")

bot.delete_webhook()
print("WEBHOOK DELETED")
