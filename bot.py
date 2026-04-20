import telebot
import os

# جلب التوكن من Railway Variables
TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    print("❌ BOT_TOKEN is missing!")
    exit()

bot = telebot.TeleBot(TOKEN)

print("BOT IS RUNNING")

# اختبار استقبال أي رسالة
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    print("🔥 MESSAGE RECEIVED")
    print("TYPE:", message.content_type)

    if message.content_type == "photo":
        file_id = message.photo[-1].file_id
        print("📸 FILE ID:", file_id)
        bot.reply_to(message, file_id)
    else:
        bot.reply_to(message, "ارسل صورة حتى أطلع file_id")

# تنظيف أي webhook قديم
bot.remove_webhook()

print("STARTING POLLING...")

# تشغيل البوت
bot.infinity_polling(skip_pending=True)
