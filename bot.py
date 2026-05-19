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
    "الفجر": "AgACAgQAAxkBAAPDagx24sOAWya1m2Yu48bpMw3CunAAAhgOaxvXwWBQKjMRp_ZwV5kBAAMCAAN5AAM7BA",
    "الظهر": "AgACAgQAAxkBAAPBagx20q9M2h6faJBEp2z7wUqMZFkAAhcOaxvXwWBQdckhJVTTd-YBAAMCAAN5AAM7BA",
    "العصر": "AgACAgQAAxkBAAO8agx2d8aNz3wvXZLm7p8aBu2ckqoAAhUOaxvXwWBQiTznM307y_wBAAMCAAN5AAM7BA",
    "المغرب": "AgACAgQAAxkBAAPFagx28cAt1uc7UJW93m9MsHhtSmAAAhkOaxvXwWBQ2Aqi_3Sml60BAAMCAAN5AAM7BA",
    "العشاء": "AgACAgQAAxkBAAO_agx2vskAAX8S5CgRe_G06uVI3Z-pAAIWDmsb18FgUOhHmqp4-IqqAQADAgADeQADOwQ",
}

# =========================
# جدول الشهر
# =========================
monthly_times = {
    1:  {"الفجر": "03:36", "الظهر": "12:05", "العصر": "15:47", "المغرب": "18:54", "العشاء": "20:18"},
    2:  {"الفجر": "03:35", "الظهر": "12:04", "العصر": "15:48", "المغرب": "18:55", "العشاء": "20:19"},
    3:  {"الفجر": "03:34", "الظهر": "12:04", "العصر": "15:48", "المغرب": "18:56", "العشاء": "20:20"},
    4:  {"الفجر": "03:32", "الظهر": "12:04", "العصر": "15:48", "المغرب": "18:57", "العشاء": "20:21"},
    5:  {"الفجر": "03:31", "الظهر": "12:04", "العصر": "15:48", "المغرب": "18:58", "العشاء": "20:22"},
    6:  {"الفجر": "03:29", "الظهر": "12:04", "العصر": "15:48", "المغرب": "18:58", "العشاء": "20:23"},
    7:  {"الفجر": "03:28", "الظهر": "12:04", "العصر": "15:48", "المغرب": "18:59", "العشاء": "20:25"},
    8:  {"الفجر": "03:27", "الظهر": "12:04", "العصر": "15:48", "المغرب": "19:00", "العشاء": "20:26"},
    9:  {"الفجر": "03:26", "الظهر": "12:04", "العصر": "15:48", "المغرب": "19:01", "العشاء": "20:27"},
    10: {"الفجر": "03:24", "الظهر": "12:04", "العصر": "15:48", "المغرب": "19:02", "العشاء": "20:28"},
    11: {"الفجر": "03:23", "الظهر": "12:04", "العصر": "15:49", "المغرب": "19:03", "العشاء": "20:29"},
    12: {"الفجر": "03:22", "الظهر": "12:04", "العصر": "15:49", "المغرب": "19:03", "العشاء": "20:30"},
    13: {"الفجر": "03:21", "الظهر": "12:04", "العصر": "15:49", "المغرب": "19:04", "العشاء": "20:31"},
    14: {"الفجر": "03:19", "الظهر": "12:04", "العصر": "15:49", "المغرب": "19:05", "العشاء": "20:33"},
    15: {"الفجر": "03:18", "الظهر": "12:04", "العصر": "15:49", "المغرب": "19:06", "العشاء": "20:34"},
    16: {"الفجر": "03:17", "الظهر": "12:04", "العصر": "15:49", "المغرب": "19:07", "العشاء": "20:35"},
    17: {"الفجر": "03:16", "الظهر": "12:04", "العصر": "15:49", "المغرب": "19:07", "العشاء": "20:36"},
    18: {"الفجر": "03:15", "الظهر": "12:04", "العصر": "15:50", "المغرب": "19:08", "العشاء": "20:37"},
    19: {"الفجر": "03:14", "الظهر": "12:04", "العصر": "15:50", "المغرب": "19:09", "العشاء": "20:38"},
    20: {"الفجر": "03:13", "الظهر": "12:04", "العصر": "15:50", "المغرب": "19:10", "العشاء": "20:39"},
    21: {"الفجر": "03:12", "الظهر": "12:04", "العصر": "15:50", "المغرب": "19:11", "العشاء": "20:40"},
    22: {"الفجر": "03:11", "الظهر": "12:04", "العصر": "15:50", "المغرب": "19:11", "العشاء": "20:41"},
    23: {"الفجر": "03:10", "الظهر": "12:04", "العصر": "15:50", "المغرب": "19:12", "العشاء": "20:42"},
    24: {"الفجر": "03:09", "الظهر": "12:04", "العصر": "15:50", "المغرب": "19:13", "العشاء": "20:43"},
    25: {"الفجر": "03:08", "الظهر": "12:04", "العصر": "15:51", "المغرب": "19:13", "العشاء": "20:44"},
    26: {"الفجر": "03:07", "الظهر": "12:05", "العصر": "15:51", "المغرب": "19:14", "العشاء": "20:45"},
    27: {"الفجر": "03:07", "الظهر": "12:05", "العصر": "15:51", "المغرب": "19:15", "العشاء": "20:46"},
    28: {"الفجر": "03:06", "الظهر": "12:05", "العصر": "15:51", "المغرب": "19:16", "العشاء": "20:47"},
    29: {"الفجر": "03:05", "الظهر": "12:05", "العصر": "15:51", "المغرب": "19:16", "العشاء": "20:48"},
    30: {"الفجر": "03:04", "الظهر": "12:05", "العصر": "15:51", "المغرب": "19:17", "العشاء": "20:49"},
    31: {"الفجر": "03:04", "الظهر": "12:05", "العصر": "15:52", "المغرب": "19:18", "العشاء": "20:50"},
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
    try:
        bot.remove_webhook()
        logger.info("Webhook removed")
    except Exception as e:
        logger.warning(f"remove_webhook warning: {e}")

    prayer_thread = threading.Thread(target=run_prayer_loop, daemon=True)
    prayer_thread.start()

    logger.info("STARTING POLLING...")

    try:
        bot.infinity_polling(
            skip_pending=True,
            timeout=30,
            long_polling_timeout=30,
            logger_level=logging.INFO,
        )

    except ApiTelegramException as e:
        logger.error(f"Polling Telegram error: {e}")
        logger.error(traceback.format_exc())

        if "409" in str(e) or "Conflict" in str(e):
            logger.error("يوجد نسخة ثانية من نفس البوت شغالة. أوقف النسخة القديمة.")
            sys.exit(1)

        time.sleep(5)
        main()

    except Exception as e:
        logger.error(f"Polling crashed: {e}")
        logger.error(traceback.format_exc())
        time.sleep(5)
        main()


if __name__ == "__main__":
    main()
