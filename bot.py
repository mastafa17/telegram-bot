import telebot

TOKEN = "BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

# لما المستخدم يرسل صورة
@bot.message_handler(content_types=['photo'])
def get_file_id(message):
    # الصورة تجي بعدة أحجام، ناخذ أعلى جودة (آخر وحدة)
    file_id = message.photo[-1].file_id
    
    bot.reply_to(message, f"📸 File ID:\n{file_id}")

# تشغيل البوت
print("Bot is running...")
bot.infinity_polling()
