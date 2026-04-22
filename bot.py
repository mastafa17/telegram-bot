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
