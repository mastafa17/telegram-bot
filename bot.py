import telebot
import os

# جلب التوكن من Railway Variables
TOKEN = os.getenv("BOT_TOKEN")

# إنشاء البوت
bot = telebot.TeleBot(TOKEN)

print("BOT STARTED")

# استقبال أي رسالة (للتأكد أنه شغال)
@bot.message_handler(func=lambda message: True)
def all_messages(message):
    print("MESSAGE TYPE:", message.content_type)

    # إذا صورة
    if message.content_type == "photo":
        file_id = message.photo[-1].file_id
        print("FILE ID:", file_id)

        bot.reply_to(message, f"FILE ID:\n{file_id}")
    else:
        bot.reply_to(message, "ارسل صورة حتى أطلع file_id")

# تنظيف أي webhook قديم
bot.remove_webhook()

print("STARTING POLLING...")

# تشغيل البوت
bot.infinity_polling(skip_pending=True)
