import os
import sys
import time
import threading
import logging
import traceback
from datetime import datetime

import pytz
import telebot

# =========================
# إعدادات عامة
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("prayer-bot")

IRAQ_TZ = pytz.timezone("Asia/Baghdad")
CHECK_INTERVAL = 20  # ثواني

# =========================
# متغيرات البيئة
# =========================
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID_RAW = os.getenv("CHAT_ID")

if not TOKEN:
    logger.error("BOT_TOKEN is missing")
    sys.exit(1)

if not CHAT_ID_RAW:
    logger.error("CHAT_ID is missing")
    sys.exit(1)

try:
    CHAT_ID = int(CHAT_ID_RAW)
except ValueError:
    CHAT_ID = CHAT_ID_RAW

bot = telebot.TeleBot(TOKEN)

print("BOT STARTED")

# =========================
# صور الصلوات
# ضع file_id الصحيح لكل صورة
# =========================
images = {
    "الفجر": "AgACAgQAAyEFAATra2AKAAMLaeZTnpGPdOL-q4hiAAHimtcBeHDCAAK4DGsbwe0wUxnuS0NczijbAQADAgADeAADOwQ",
    "الظهر": "AgACAgQAAyEFAATra2AKAAMWaeZajlCubRzED-5sBm3NxZY4b5sAAsEMaxvB7TBTnPJ4f2LSSnwBAAMCAAN4AAM7BA",
    "العصر": "AgACAgQAAyEFAATra2AKAAMVaeZaIAmK2Z0mTVqDvfcsaqTlocEAAsAMaxvB7TBT5uG2_1rDNsUBAAMCAAN4AAM7BA",
    "المغرب": "AgACAgQAAyEFAATra2AKAAMlaeZgEN4lyS9TksS_IPb4Vrrb3xEAAskMaxvB7TBTrlnQl6_sZyUBAAMCAAN4AAM7BA",
    "العشاء": "AgACAgQAAyEFAATra2AKAAMXaeZapoas3WYoHbZAbqurFZCx0hUAAsIMaxvB7TBT5wQnB20X3Y4BAAMCAAN4AAM7BA",
}

# =========================
# جدول الشهور
# =========================
monthly_times = {
    1:  {"الفجر":"03:36","الظهر":"12:05","العصر":"15:47","المغرب":"18:54","العشاء":"20:18"},
    2:  {"الفجر":"03:35","الظهر":"12:04","العصر":"15:48","المغرب":"18:55","العشاء":"20:19"},
    3:  {"الفجر":"03:34","الظهر":"12:04","العصر":"15:48","المغرب":"18:56","العشاء":"20:20"},
    4:  {"الفجر":"03:32","الظهر":"12:04","العصر":"15:48","المغرب":"18:57","العشاء":"20:21"},
    5:  {"الفجر":"03:31","الظهر":"12:04","العصر":"15:48","المغرب":"18:58","العشاء":"20:22"},
    6:  {"الفجر":"03:29","الظهر":"12:04","العصر":"15:48","المغرب":"18:58","العشاء":"20:23"},
    7:  {"الفجر":"03:28","الظهر":"12:04","العصر":"15:48","المغرب":"18:59","العشاء":"20:25"},
    8:  {"الفجر":"03:27","الظهر":"12:04","العصر":"15:48","المغرب":"19:00","العشاء":"20:26"},
    9:  {"الفجر":"03:26","الظهر":"12:04","العصر":"15:48","المغرب":"19:01","العشاء":"20:27"},
    10: {"الفجر":"03:24","الظهر":"12:04","العصر":"15:48","المغرب":"19:02","العشاء":"20:28"},
    11: {"الفجر":"03:23","الظهر":"12:04","العصر":"15:49","المغرب":"19:03","العشاء":"20:29"},
    12: {"الفجر":"03:22","الظهر":"12:04","العصر":"15:49","المغرب":"19:03","العشاء":"20:30"},
    13: {"الفجر":"03:21","الظهر":"12:04","العصر":"15:49","المغرب":"19:04","العشاء":"20:31"},
    14: {"الفجر":"03:19","الظهر":"12:04","العصر":"15:49","المغرب":"19:05","العشاء":"20:33"},
    15: {"الفجر":"03:18","الظهر":"12:04","العصر":"15:49","المغرب":"19:06","العشاء":"20:34"},
    16: {"الفجر":"03:17","الظهر":"12:04","العصر":"15:49","المغرب":"19:07","العشاء":"20:35"},
    17: {"الفجر":"03:16","الظهر":"12:04","العصر":"15:49","المغرب":"19:07","العشاء":"20:36"},
    18: {"الفجر":"03:15","الظهر":"12:04","العصر":"15:50","المغرب":"19:08","العشاء":"20:37"},
    19: {"الفجر":"03:14","الظهر":"12:04","العصر":"15:50","المغرب":"19:09","العشاء":"20:38"},
    20: {"الفجر":"03:13","الظهر":"12:04","العصر":"15:50","المغرب":"19:10","العشاء":"20:39"},
    21: {"الفجر":"03:12","الظهر":"12:04","العصر":"15:50","المغرب":"19:11","العشاء":"20:40"},
    22: {"الفجر":"03:11","الظهر":"12:04","العصر":"15:50","المغرب":"19:11","العشاء":"20:41"},
    23: {"الفجر":"03:10","الظهر":"12:04","العصر":"15:50","المغرب":"19:12","العشاء":"20:42"},
    24: {"الفجر":"03:09","الظهر":"12:04","العصر":"15:50","المغرب":"19:13","العشاء":"20:43"},
    25: {"الفجر":"03:08","الظهر":"12:04","العصر":"15:51","المغرب":"19:13","العشاء":"20:44"},
    26: {"الفجر":"03:07","الظهر":"12:05","العصر":"15:51","المغرب":"19:14","العشاء":"20:45"},
    27: {"الفجر":"03:07","الظهر":"12:05","العصر":"15:51","المغرب":"19:15","العشاء":"20:46"},
    28: {"الفجر":"03:06","الظهر":"12:05","العصر":"15:51","المغرب":"19:16","العشاء":"20:47"},
    29: {"الفجر":"03:05","الظهر":"12:05","العصر":"15:51","المغرب":"19:16","العشاء":"20:48"},
    30: {"الفجر":"03:04","الظهر":"12:05","العصر":"15:51","المغرب":"19:17","العشاء":"20:49"},
    31: {"الفجر":"03:04","الظهر":"12:05","العصر":"15:52","المغرب":"19:18","العشاء":"20:50"},
}

PRAYERS = ["الفجر", "الظهر", "العصر", "المغرب", "العشاء"]
last_sent = set()
lock = threading.Lock()

# =========================
# دوال مساعدة
# =========================
def now_iraq() -> datetime:
    return datetime.now(IRAQ_TZ)


def format_time_12h(time_str: str) -> str:
    t = datetime.strptime(time_str, "%H:%M")
    hour = int(t.strftime("%H"))
    period = "صباحاً" if hour < 12 else "مساءً"
    return t.strftime("%I:%M") + f" {period}"


def get_today_times() -> dict:
    day = now_iraq().day
    return monthly_times.get(day, {})


def send_adhan(prayer: str) -> bool:
    """يرسل صورة الصلاة مع النص. يرجع True إذا تم الإرسال."""
    try:
        day = now_iraq().day
        today_times = monthly_times.get(day)

        if not today_times:
            logger.warning(f"No schedule found for day {day}")
            return False

        time_now = today_times.get(prayer)
        if not time_now:
            logger.warning(f"No time found for prayer={prayer} on day={day}")
            return False

        file_id = images.get(prayer)
        if not file_id:
            logger.warning(f"No image file_id found for prayer={prayer}")
            return False

        time_12 = format_time_12h(time_now)
        text = f"حان الآن موعد صلاة {prayer} 🕌\nالوقت: {time_12} ⏰"

        bot.send_photo(CHAT_ID, file_id, caption=text)
        logger.info(f"Sent: {prayer}")
        return True

    except Exception as e:
        logger.error(f"send_adhan error for {prayer}: {e}")
        logger.error(traceback.format_exc())
        return False


def check_prayers():
    now = now_iraq()
    current_time = now.strftime("%H:%M")
    day = now.day
    today_times = monthly_times.get(day, {})

    for prayer, prayer_time in today_times.items():
        if current_time == prayer_time:
            key = f"{day}_{prayer}"
            with lock:
                already_sent = key in last_sent
                if not already_sent:
                    if send_adhan(prayer):
                        last_sent.add(key)


def clean_old_sent_markers():
    """تنظيف العلامات القديمة حتى لا يكبر الذاكرة مع الوقت."""
    current_day = now_iraq().day
    with lock:
        old_keys = {k for k in last_sent if not k.startswith(f"{current_day}_")}
        if old_keys:
            last_sent.difference_update(old_keys)


def run_loop():
    logger.info("Prayer loop started")
    while True:
        try:
            check_prayers()
            clean_old_sent_markers()
        except Exception as e:
            logger.error(f"Loop error: {e}")
            logger.error(traceback.format_exc())
        time.sleep(CHECK_INTERVAL)


# =========================
# أوامر البوت
# =========================
@bot.message_handler(commands=["start"])
def start(msg):
    text = (
        "أهلاً بك 👋\n\n"
        "هذا بوت مواقيت الصلاة.\n"
        "الأوامر المتاحة:\n"
        "/test_all - إرسال كل الصلوات\n"
        "/test - إرسال العشاء فقط\n"
        "/today - عرض مواقيت اليوم"
    )
    bot.reply_to(msg, text)


@bot.message_handler(commands=["today"])
def today(msg):
    times = get_today_times()
    if not times:
        bot.reply_to(msg, "ما لقيت جدول لليوم.")
        return

    lines = ["مواقيت اليوم:\n"]
    for prayer in PRAYERS:
        t = times.get(prayer)
        if t:
            lines.append(f"{prayer}: {format_time_12h(t)}")
    bot.reply_to(msg, "\n".join(lines))


@bot.message_handler(commands=["test_all"])
def test_all(msg):
    for prayer in PRAYERS:
        send_adhan(prayer)
        time.sleep(1)


@bot.message_handler(commands=["test"])
def test(msg):
    send_adhan("العشاء")


# =========================
# التشغيل
# =========================
def main():
    try:
        bot.remove_webhook()
        logger.info("Webhook removed")
    except Exception as e:
        logger.warning(f"remove_webhook warning: {e}")

    threading.Thread(target=run_loop, daemon=True).start()
    logger.info("STARTING POLLING...")

    while True:
        try:
            bot.infinity_polling(
                skip_pending=True,
                timeout=30,
                long_polling_timeout=30,
                logger_level=logging.INFO,
            )
        except Exception as e:
            logger.error(f"Polling crashed: {e}")
            logger.error(traceback.format_exc())
            time.sleep(5)


if __name__ == "__main__":
    main()
