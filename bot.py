import telebot
import os
import time
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
    21: {"الفجر":"03:51","الظهر":"12:06","العصر":"15:46","المغرب":"18:46","العشاء":"20:12"},
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

    if today not in monthly_times:
        return

    time_now = monthly_times[today][prayer]
    time_12 = to_12_hour(time_now)

    text = (
        f"حان الآن موعد صلاة {prayer} 🕌\n"
        f"الوقت: {time_12} ⏰"
    )

    try:
        bot.send_photo(CHAT_ID, images[prayer], caption=text)
        print(f"Sent {prayer} at {time_12}")
    except Exception as e:
        print("Error:", e)

# ================== النظام الجديد (بديل schedule) ==================
sent_today = {}

def check_adhan():
    now = datetime.now(iraq_tz)
    today = now.day
    current_time = now.strftime("%H:%M")

    if today not in monthly_times:
        return

    for prayer, t in monthly_times[today].items():
        key = f"{today}-{prayer}"

        if t == current_time and key not in sent_today:
            send_adhan(prayer)
            sent_today[key] = True

# ================== loop ==================
def run_loop():
    print("ADHAN SYSTEM RUNNING...")
    while True:
        check_adhan()
        time.sleep(20)

# ================== أوامر التليجرام ==================

@bot.message_handler(commands=['test_all'])
def test_all(msg):
    for prayer in ["الفجر", "الظهر", "العصر", "المغرب", "العشاء"]:
        send_adhan(prayer)

@bot.message_handler(commands=['test'])
def test(msg):
    send_adhan("العشاء")

# ================== تشغيل ==================
threading.Thread(target=run_loop).start()

bot.remove_webhook()
time.sleep(1)

print("BOT READY")
bot.polling(none_stop=True)
