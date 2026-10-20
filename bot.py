import os
import sys
import time
import threading
import logging
import traceback
from datetime import datetime

import pytz
import telebot
from telebot.apihelper import ApiTelegramException

# =========================
# إعدادات عامة
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("prayer-bot")

IRAQ_TZ = pytz.timezone("Asia/Baghdad")
CHECK_INTERVAL = 20  # كل 20 ثانية يفحص وقت الصلاة

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

bot = telebot.TeleBot(TOKEN, parse_mode=None)

logger.info("BOT STARTED")

# =========================
# صور الصلوات
# =========================
images = {
    "الفجر": "AgACAgQAAyEFAATra2AKAAMLaeZTnpGPdOL-q4hiAAHimtcBeHDCAAK4DGsbwe0wUxnuS0NczijbAQADAgADeAADOwQ",
    "الظهر": "AgACAgQAAyEFAATra2AKAAMWaeZajlCubRzED-5sBm3NxZY4b5sAAsEMaxvB7TBTnPJ4f2LSSnwBAAMCAAN4AAM7BA",
    "العصر": "AgACAgQAAyEFAATra2AKAAMVaeZaIAmK2Z0mTVqDvfcsaqTlocEAAsAMaxvB7TBT5uG2_1rDNsUBAAMCAAN4AAM7BA",
    "المغرب": "AgACAgQAAyEFAATra2AKAAMlaeZgEN4lyS9TksS_IPb4Vrrb3xEAAskMaxvB7TBTrlnQl6_sZyUBAAMCAAN4AAM7BA",
    "العشاء": "AgACAgQAAyEFAATra2AKAAMXaeZapoas3WYoHbZAbqurFZCx0hUAAsIMaxvB7TBT5wQnB20X3Y4BAAMCAAN4AAM7BA",
}

# =========================
# جدول الشهر
# =========================
monthly_times = {
    1:  {"الفجر":"04:33","الشروق":"05:54","الظهر":"11:57","العصر":"15:16","المغرب":"17:52","العشاء":"19:06"},
    2:  {"الفجر":"04:33","الشروق":"05:55","الظهر":"11:57","العصر":"15:15","المغرب":"17:50","العشاء":"19:04"},
    3:  {"الفجر":"04:34","الشروق":"05:56","الظهر":"11:56","العصر":"15:15","المغرب":"17:49","العشاء":"19:03"},
    4:  {"الفجر":"04:35","الشروق":"05:56","الظهر":"11:56","العصر":"15:14","المغرب":"17:47","العشاء":"19:02"},
    5:  {"الفجر":"04:36","الشروق":"05:57","الظهر":"11:56","العصر":"15:13","المغرب":"17:46","العشاء":"19:00"},
    6:  {"الفجر":"04:37","الشروق":"05:58","الظهر":"11:56","العصر":"15:12","المغرب":"17:45","العشاء":"18:59"},
    7:  {"الفجر":"04:38","الشروق":"05:59","الظهر":"11:55","العصر":"15:11","المغرب":"17:43","العشاء":"18:57"},
    8:  {"الفجر":"04:38","الشروق":"06:00","الظهر":"11:55","العصر":"15:10","المغرب":"17:42","العشاء":"18:56"},
    9:  {"الفجر":"04:39","الشروق":"06:00","الظهر":"11:55","العصر":"15:09","المغرب":"17:41","العشاء":"18:55"},
    10: {"الفجر":"04:40","الشروق":"06:01","الظهر":"11:54","العصر":"15:08","المغرب":"17:39","العشاء":"18:53"},
    11: {"الفجر":"04:41","الشروق":"06:02","الظهر":"11:54","العصر":"15:07","المغرب":"17:38","العشاء":"18:52"},
    12: {"الفجر":"04:42","الشروق":"06:03","الظهر":"11:54","العصر":"15:06","المغرب":"17:36","العشاء":"18:51"},
    13: {"الفجر":"04:42","الشروق":"06:04","الظهر":"11:54","العصر":"15:05","المغرب":"17:35","العشاء":"18:49"},
    14: {"الفجر":"04:43","الشروق":"06:04","الظهر":"11:53","العصر":"15:04","المغرب":"17:34","العشاء":"18:48"},
    15: {"الفجر":"04:44","الشروق":"06:05","الظهر":"11:53","العصر":"15:03","المغرب":"17:33","العشاء":"18:47"},
    16: {"الفجر":"04:45","الشروق":"06:06","الظهر":"11:53","العصر":"15:02","المغرب":"17:31","العشاء":"18:46"},
    17: {"الفجر":"04:46","الشروق":"06:07","الظهر":"11:53","العصر":"15:01","المغرب":"17:30","العشاء":"18:44"},
    18: {"الفجر":"04:46","الشروق":"06:08","الظهر":"11:53","العصر":"15:00","المغرب":"17:29","العشاء":"18:43"},
    19: {"الفجر":"04:47","الشروق":"06:09","الظهر":"11:52","العصر":"14:59","المغرب":"17:28","العشاء":"18:42"},
    20: {"الفجر":"04:48","الشروق":"06:10","الظهر":"11:52","العصر":"14:58","المغرب":"17:26","العشاء":"18:41"},
    21: {"الفجر":"04:49","الشروق":"06:11","الظهر":"11:52","العصر":"14:57","المغرب":"17:25","العشاء":"18:40"},
    22: {"الفجر":"04:50","الشروق":"06:11","الظهر":"11:52","العصر":"14:56","المغرب":"17:24","العشاء":"18:39"},
    23: {"الفجر":"04:51","الشروق":"06:12","الظهر":"11:52","العصر":"14:55","المغرب":"17:23","العشاء":"18:38"},
    24: {"الفجر":"04:51","الشروق":"06:13","الظهر":"11:52","العصر":"14:54","المغرب":"17:22","العشاء":"18:36"},
    25: {"الفجر":"04:52","الشروق":"06:14","الظهر":"11:52","العصر":"14:53","المغرب":"17:20","العشاء":"18:35"},
    26: {"الفجر":"04:53","الشروق":"06:15","الظهر":"11:51","العصر":"14:53","المغرب":"17:19","العشاء":"18:34"},
    27: {"الفجر":"04:54","الشروق":"06:16","الظهر":"11:51","العصر":"14:52","المغرب":"17:18","العشاء":"18:33"},
    28: {"الفجر":"04:55","الشروق":"06:17","الظهر":"11:51","العصر":"14:51","المغرب":"17:17","العشاء":"18:32"},
    29: {"الفجر":"04:55","الشروق":"06:18","الظهر":"11:51","العصر":"14:50","المغرب":"17:16","العشاء":"18:31"},
    30: {"الفجر":"04:56","الشروق":"06:19","الظهر":"11:51","العصر":"14:49","المغرب":"17:15","العشاء":"18:30"},
    31: {"الفجر":"04:57","الشروق":"06:20","الظهر":"11:51","العصر":"14:48","المغرب":"17:14","العشاء":"18:30"},
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


def build_caption(prayer: str, prayer_time: str) -> str:
    time_12 = format_time_12h(prayer_time)
    return f"حان الآن موعد صلاة {prayer} 🕌\nالوقت: {time_12} ⏰"


def send_adhan(prayer: str, target_chat_id=None) -> bool:
    """
    target_chat_id = None  يعني إرسال للقناة
    target_chat_id موجود يعني إرسال خاص للاختبار
    """
    try:
        day = now_iraq().day
        today_times = monthly_times.get(day)

        if not today_times:
            logger.warning(f"No schedule found for day {day}")
            return False

        prayer_time = today_times.get(prayer)
        if not prayer_time:
            logger.warning(f"No time found for prayer={prayer} on day={day}")
            return False

        file_id = images.get(prayer)
        if not file_id:
            logger.warning(f"No image found for prayer={prayer}")
            return False

        caption = build_caption(prayer, prayer_time)
        send_to = target_chat_id if target_chat_id is not None else CHAT_ID

        logger.info(f"Sending prayer={prayer}")
        logger.info(f"Target chat={send_to}")
        logger.info(f"Using file_id={file_id}")

        bot.send_photo(send_to, file_id, caption=caption)

        logger.info(f"Sent successfully: {prayer}")
        return True

    except ApiTelegramException as e:
        logger.error(f"Telegram error while sending {prayer}: {e}")
        logger.error(traceback.format_exc())
        return False

    except Exception as e:
        logger.error(f"Unknown error while sending {prayer}: {e}")
        logger.error(traceback.format_exc())
        return False


# =========================
# نظام الإرسال التلقائي
# =========================
def check_prayers():
    now = now_iraq()
    current_time = now.strftime("%H:%M")
    current_day = now.day

    today_times = monthly_times.get(current_day, {})
    if not today_times:
        return

    for prayer in PRAYERS:
        prayer_time = today_times.get(prayer)

        if not prayer_time:
            continue

        if current_time == prayer_time:
            key = f"{now.strftime('%Y-%m-%d')}_{prayer}"

            with lock:
                if key in last_sent:
                    continue

                sent = send_adhan(prayer)

                if sent:
                    last_sent.add(key)


def clean_old_sent_markers():
    today_prefix = now_iraq().strftime("%Y-%m-%d")

    with lock:
        old_keys = {k for k in last_sent if not k.startswith(today_prefix)}

        if old_keys:
            last_sent.difference_update(old_keys)
            logger.info(f"Cleaned old sent markers: {len(old_keys)}")


def run_prayer_loop():
    logger.info("Prayer loop started")

    while True:
        try:
            check_prayers()
            clean_old_sent_markers()
        except Exception as e:
            logger.error(f"Prayer loop error: {e}")
            logger.error(traceback.format_exc())

        time.sleep(CHECK_INTERVAL)


# =========================
# أوامر البوت
# =========================
@bot.message_handler(commands=["start"])
def start(msg):
    text = (
        "أهلاً بك 👋\n\n"
        "هذا بوت مواقيت الصلاة.\n\n"
        "الأوامر:\n"
        "/today - عرض مواقيت اليوم\n"
        "/test المغرب - اختبار صورة صلاة معينة بالخاص\n"
        "/test_all - اختبار كل الصور بالخاص\n\n"
        "ملاحظة: الاختبار يرسل لك أنت فقط، وليس للقناة."
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
        prayer_time = times.get(prayer)
        if prayer_time:
            lines.append(f"{prayer}: {format_time_12h(prayer_time)}")

    bot.reply_to(msg, "\n".join(lines))


@bot.message_handler(commands=["test"])
def test(msg):
    """
    مثال:
    /test المغرب
    يرسل الصورة إلى صاحب الأمر بالخاص فقط
    """
    user_id = msg.from_user.id if msg.from_user else None

    if not user_id:
        bot.reply_to(msg, "ما قدرت أعرف المستخدم.")
        return

    parts = msg.text.split(maxsplit=1)

    if len(parts) < 2:
        bot.reply_to(
            msg,
            "اكتب اسم الصلاة بعد الأمر، مثل:\n\n"
            "/test الفجر\n"
            "/test الظهر\n"
            "/test العصر\n"
            "/test المغرب\n"
            "/test العشاء"
        )
        return

    prayer = parts[1].strip()

    if prayer not in PRAYERS:
        bot.reply_to(
            msg,
            "اسم الصلاة غير صحيح.\n\n"
            "استخدم واحد من هذه الأسماء بالضبط:\n"
            "الفجر\n"
            "الظهر\n"
            "العصر\n"
            "المغرب\n"
            "العشاء"
        )
        return

    bot.reply_to(msg, f"جاري إرسال اختبار صلاة {prayer} إلى الخاص...")

    ok = send_adhan(prayer, target_chat_id=user_id)

    if ok:
        if msg.chat.id != user_id:
            bot.reply_to(msg, "تم إرسال الاختبار بالخاص ✅")
    else:
        bot.reply_to(
            msg,
            "ما قدرت أرسل لك بالخاص.\n"
            "افتح محادثة البوت واضغط /start ثم جرب مرة ثانية."
        )


@bot.message_handler(commands=["test_all"])
def test_all(msg):
    """
    يرسل كل الصور لصاحب الأمر بالخاص فقط
    """
    user_id = msg.from_user.id if msg.from_user else None

    if not user_id:
        bot.reply_to(msg, "ما قدرت أعرف المستخدم.")
        return

    bot.reply_to(msg, "جاري إرسال كل صور الصلوات إلى الخاص...")

    all_ok = True

    for prayer in PRAYERS:
        ok = send_adhan(prayer, target_chat_id=user_id)
        if not ok:
            all_ok = False
        time.sleep(1)

    if all_ok:
        if msg.chat.id != user_id:
            bot.reply_to(msg, "تم إرسال كل الاختبارات بالخاص ✅")
    else:
        bot.reply_to(
            msg,
            "بعض الصور ما انرسلت.\n"
            "افتح الخاص ويا البوت واضغط /start، ثم جرب مرة ثانية."
        )


@bot.message_handler(content_types=["photo"])
def get_photo_file_id(msg):
    """
    هذا يفيدك حتى تجيب file_id لأي صورة جديدة.
    ارسل الصورة للبوت بالخاص، وهو يرجع لك file_id.
    """
    try:
        photo = msg.photo[-1]
        file_id = photo.file_id

        bot.reply_to(
            msg,
            "File ID للصورة:\n\n"
            f"{file_id}"
        )

        logger.info(f"New photo file_id: {file_id}")

    except Exception as e:
        logger.error(f"get_photo_file_id error: {e}")
        logger.error(traceback.format_exc())
        bot.reply_to(msg, "صار خطأ أثناء استخراج file_id.")


# =========================
# التشغيل
# =========================
def main():
    logger.info("BOT STARTED")

    # إزالة الـ Webhook مرة واحدة قبل بدء Polling
    try:
        bot.remove_webhook()
        logger.info("Webhook removed")
    except Exception:
        logger.exception("Webhook removal failed")
        raise

    prayer_thread = threading.Thread(
        target=run_prayer_loop,
        daemon=True,
        name="prayer-loop",
    )
    prayer_thread.start()

    logger.info("STARTING POLLING...")

    # لا تعاود تشغيل Polling تلقائياً عند تعارض 409
    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30,
        logger_level=logging.INFO,
    )


if __name__ == "__main__":
    try:
        main()
    except ApiTelegramException as e:
        logger.critical("Telegram API error: %s", e)
        if "409" in str(e) or "Conflict" in str(e):
            logger.critical(
                "Polling conflict: check for another running bot instance."
            )
        sys.exit(1)
    except Exception:
        logger.exception("Fatal bot error")
        sys.exit(1)
