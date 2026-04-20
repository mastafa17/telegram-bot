
import telebot

bot = telebot.TeleBot("8559357103:AAGTeH5u4DiwDYZDBSDn4z1O7P3pBXwDse4")

print("BOT STARTED")  # 👈 هنا حطه

bot.remove_webhook()

@bot.message_handler(content_types=['photo', 'document', 'text'])
def handler(message):
    print("RECEIVED:", message.content_type)

bot.infinity_polling()
