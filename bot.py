import time
import requests
import xml.etree.ElementTree as ET

TOKEN = "8559357103:AAGTeH5u4DiwDYZDBSDn4z1O7P3pBXwDse4"
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

            return title, link

    except Exception as e:
        print("RSS error:", e)

    return None, None


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)


while True:
    title, link = get_latest_post()

    if link and link != last_link:
        msg = f"{title}\n{link}"
        send_message(msg)
        last_link = link
        print("📩 تم إرسال منشور جديد")

    time.sleep(60)
