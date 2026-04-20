import telebot
import os
import time
import schedule
import threading

# ================== الإعدادات ==================
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID") 

bot = telebot.TeleBot(TOKEN)

print("BOT STARTED")

# ================== بيانات الصلوات ==================
prayers = {
    "الفجر": {
        "time": "05:20",
        "file_id": "AgACAgQAAyEFAATra2AKAAMLaeZTnpGPdOL-q4hiAAHimtcBeHDCAAK4DGsbwe0wUxnuS0NczijbAQADAgADeAADOwQ"
    },
    "الظهر": {
        "time": "12:06",
        "file_id": "AgACAgQAAyEFAATra2AKAAMWaeZajlCubRzED-5sBm3NxZY4b5sAAsEMaxvB7TBTnPJ4f2LSSnwBAAMCAAN4AAM7BA"
    },
    "العصر": {
        "time": "15:46",
        "file_id": "AgACAgQAAyEFAATra2AKAAMVaeZaIAmK2Z0mTVqDvfcsaqTlocEAAsAMaxvB7TBT5uG2_1rDNsUBAAMCAAN4AAM7BA"
    },
    "المغرب": {
        "time": "18:45",
        "file_id": "AgACAgQAAyEFAATra2AKAAMlaeZgEN4lyS9TksS_IPb4Vrrb3xEAAskMaxvB7TBTrlnQl6_sZyUBAAMCAAN4AAM7BA"
    },
    "العشاء": {
        "time": "20:05",
        "file_id": "AgACAgQAAyEFAATra2AKAAMXaeZapoas3WYoHbZAbqurFZCx0hUAAsIMaxvB7TBT5wQnB20X3Y4BAAMCAAN4AAM7BA"
    }
}

# ================== إرسال الأذان ==================
def send_adhan(prayer_name):
    prayer = prayers[prayer_name]

    text = f"🕌 حان الآن موعد صلاة {prayer_name}"

    try:
        bot.send_photo(
            CHAT_ID,
            prayer["file_id"],
            caption=text
        )
        print(f"✅ Sent {prayer_name}")
    except Exception as e:
        print("❌ Error sending:", e)

# ================== الجدولة ==================
for name, data in prayers.items():
    schedule.every().day.at(data["time"]).do(send_adhan, name)

# ================== تشغيل الجدولة ==================
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule).start()

# ================== استقبال الرسائل ==================
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    print("📩 Message:", message.text)
    bot.reply_to(message, "البوت شغال 👍")

# ================== تشغيل البوت ==================
bot.remove_webhook()

print("STARTING POLLING...")

bot.infinity_polling(skip_pending=True)
