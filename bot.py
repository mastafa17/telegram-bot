import telebot

bot = telebot.TeleBot("8559357103:AAGTeH5u4DiwDYZDBSDn4z1O7P3pBXwDse4")

bot.delete_webhook()
print("WEBHOOK DELETED")
