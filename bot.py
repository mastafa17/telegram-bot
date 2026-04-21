import telebot
import os
import time
import schedule
import threading
from datetime import datetime
import pytz

iraq_tz = pytz.timezone("Asia/Baghdad")

# ================== الإعدادات ==================
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telebot.TeleBot(TOKEN)

print("BOT STARTED")

# ================== الصور ==================
images = {
    "الفجر": "AgACAgQAAyEFAATra2AKAAMLaeZTnpGPdOL-q4hiAAHimtcBeHDCAAK4DGsbwe0wUxnuS0NczijbAQADAgADeAADOwQ",
    "الظهر": "AgACAgQAAyEFAATra2AKAAMWaeZajlCubRzED-5sBm3NxZY4b5sAAsEMaxvB7TBTnPJ4f2LSSnwBAAMCAAN4AAM7BA",
    "العصر": "AgACAgQAAyEFAATra2AKAAMVaeZaIAmK2Z0mTVqDvfcsaqTlocEAAsAMaxvB7TBT5uG2_1rDNsUBAAMCAAN4AAM7BA",
    "المغرب": "AgACAgQAAyEFAATra2AKAAMlaeZgEN4lyS9TksS_IPb4Vrrb3xEAAskMaxvB7TBTrlnQl6_sZyUBAAMCAAN4AAM7BA",
    "العشاء": "AgACAgQAAyEFAATra2AKAAMXaeZapoas3WYoHbZAbqurFZCx0hUAAsIMaxvB7TBT5wQnB20X3Y4BAAMCAAN4AAM7BA"
}

# ================== مواقيت الصلاة ==================
monthly_times = {
    1:  {"الفجر":"04:23","الظهر":"12:11","العصر":"15:43","المغرب":"18:29","العشاء":"19:46"},
    2:  {"الفجر":"04:21","الظهر":"12:11","العصر":"15:44","المغرب":"18:30","العشاء":"19:47"},
    3:  {"الفجر":"04:19","الظهر":"12:11","العصر":"15:44","المغرب":"18:31","العشاء":"19:48"},
    4:  {"الفجر":"04:18","الظهر":"12:10","العصر":"15:44","المغرب":"18:32","العشاء":"19:49"},
    5:  {"الفجر":"04:16","الظهر":"12:10","العصر":"15:44","المغرب":"18:33","العشاء":"19:50"},
    6:  {"الفجر":"04:15","الظهر":"12:10","العصر":"15:44","المغرب":"18:33","العشاء":"19:51"},
    7:  {"الفجر":"04:13","الظهر":"12:10","العصر":"15:44","المغرب":"18:34","العشاء":"19:52"},
    8:  {"الفجر":"04:12","الظهر":"12:09","العصر":"15:45","المغرب":"18:35","العشاء":"19:53"},
    9:  {"الفجر":"04:10","الظهر":"12:09","العصر":"15:45","المغرب":"18:36","العشاء":"19:54"},
    10: {"الفجر":"04:08","الظهر":"12:09","العصر":"15:45","المغرب":"18:37","العشاء":"19:55"},
    11: {"الفجر":"04:07","الظهر":"12:08","العصر":"15:45","المغرب":"18:38","العشاء":"19:56"},
    12: {"الفجر":"04:05","الظهر":"12:08","العصر":"15:45","المغرب":"18:38","العشاء":"19:57"},
    13: {"الفجر":"04:04","الظهر":"12:08","العصر":"15:45","المغرب":"18:39","العشاء":"19:58"},
    14: {"الفجر":"04:02","الظهر":"12:08","العصر":"15:45","المغرب":"18:40","العشاء":"19:59"},
    15: {"الفجر":"04:00","الظهر":"12:07","العصر":"15:46","المغرب":"18:41","العشاء":"20:00"},
    16: {"الفجر":"03:59","الظهر":"12:07","العصر":"15:46","المغرب":"18:42","العشاء":"20:01"},
    17: {"الفجر":"03:57","الظهر":"12:07","العصر":"15:46","المغرب":"18:43","العشاء":"20:02"},
    18: {"الفجر":"03:56","الظهر":"12:07","العصر":"15:46","المغرب":"18:43","العشاء":"20:03"},
    19: {"الفجر":"03:54","الظهر":"12:07","العصر":"15:46","المغرب":"18:44","العشاء":"20:04"},
    20: {"الفجر":"03:53","الظهر":"12:06","العصر":"15:46","المغرب":"18:45","العشاء":"20:05"},
    21: {"الفجر":"03:51","الظهر":"12:06","العصر":"15:46","المغرب":"18:46","العشاء":"20:06"},
    22: {"الفجر":"03:50","الظهر":"12:06","العصر":"15:46","المغرب":"18:47","العشاء":"20:07"},
    23: {"الفجر":"03:48","الظهر":"12:06","العصر":"15:47","المغرب":"18:48","العشاء":"20:09"},
    24: {"الفجر":"03:47","الظهر":"12:06","العصر":"15:47","المغرب":"18:48","العشاء":"20:10"},
    25: {"الفجر":"03:45","الظهر":"12:05","العصر":"15:47","المغرب":"18:49","العشاء":"20:11"},
    26: {"الفجر":"03:44","الظهر":"12:05","العصر":"15:47","المغرب":"18:50","العشاء":"20:12"},
    27: {"الفجر":"03:42","الظهر":"12:05","العصر":"15:47","المغرب":"18:51","العشاء":"20:13"},
    28: {"الفجر":"03:41","الظهر":"12:05","العصر":"15:47","المغرب":"18:52","العشاء":"20:14"},
    29: {"الفجر":"03:39","الظهر":"12:05","العصر":"15:47","المغرب":"18:53","العشاء":"20:15"},
    30: {"الفجر":"03:38","الظهر":"12:05","العصر":"15:47","المغرب":"18:53","العشاء":"20:17"},
}

# ================== تحويل 12 ساعة ==================
def to_12_hour(time_str):
    t = datetime.strptime(time_str, "%H:%M")
    hour = int(t.strftime("%H"))

    period = "صباحاً" if hour < 12 else "مساءً"

    return t.strftime("%I:%M") + " " + period

# ================== إرسال الأذان ==================
def send_adhan(prayer):
    now = datetime.now(iraq_tz)
    today = now.day

    time_now = monthly_times[today][prayer]
    time_12 = to_12_hour(time_now)

    text = f"🕌 حان الآن موعد صلاة {prayer}\n⏰ الوقت: {time_12}"

    try:
        bot.send_photo(CHAT_ID, images[prayer], caption=text)
        print(f"Sent {prayer} at {time_12}")
    except Exception as e:
        print("Error:", e)

# ================== إعداد الجدولة ==================
def setup_today_schedule():
    print("SETTING UP SCHEDULE...")

    schedule.clear()

    now = datetime.now(iraq_tz)
    today = now.day

    today_times = monthly_times.get(today)

    if not today_times:
        print("No data for today")
        return

    for prayer, time_str in today_times.items():
        schedule.every().day.at(time_str).do(send_adhan, prayer)

    print("Schedule updated:", today_times)

# ================== تشغيل الجدولة ==================
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# ================== أوامر التليجرام ==================

# اختبار كل الصلوات
@bot.message_handler(commands=['test_all'])
def test_all(msg):
    for prayer in ["الفجر", "الظهر", "العصر", "المغرب", "العشاء"]:
        send_adhan(prayer)

# تحديث الجدول يدوياً
@bot.message_handler(commands=['reload'])
def reload_schedule(msg):
    setup_today_schedule()
    bot.send_message(msg.chat.id, "Schedule updated ✔")

# اختبار صلاة واحدة
@bot.message_handler(commands=['test'])
def test(msg):
    send_adhan("العشاء")

# ================== تشغيل النظام ==================
setup_today_schedule()
schedule.every().day.at("00:01").do(setup_today_schedule)

threading.Thread(target=run_schedule).start()

bot.remove_webhook()
time.sleep(1)

print("BOT READY")

bot.polling(none_stop=True)
