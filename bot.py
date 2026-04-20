import time
import requests
import xml.etree.ElementTree as ET

TOKEN = "AAGTeH5u4DiwDYZDBSDn4z1O7P3pBXwDse4"
CHAT_ID = "-1003949682698"
RSS_URL = "https://rss.app/feeds/8znlULlLiittrnz2.xml"

last_link = ""

def get_latest_post():
    try:
        r = requests.get(RSS_URL, timeout=10)
        root = ET.fromstring(r.content)

        for item in root.iter("item"):
            title = item.find("title").text
            link = item.find("link").text

            # جلب الصورة من RSS
            media = item.find("{http://search.yahoo.com/mrss/}content")
            image = media.get("url") if media is not None else None

            return title, link, image

    except Exception as e:
        print("RSS error:", e)

    return None, None, None


def send_photo(photo, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    data = {
        "chat_id": CHAT_ID,
        "photo": photo,
        "caption": caption
    }
    requests.post(url, data=data)


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)


while True:
    title, link, image = get_latest_post()

    if link and link != last_link:
        if image:
            send_photo(image, title)
        else:
            send_message(title)

        last_link = link
        print("📩 تم إرسال منشور جديد")

    time.sleep(30)
