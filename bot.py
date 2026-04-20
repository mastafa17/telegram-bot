import time
import requests
from bs4 import BeautifulSoup

TOKEN = "PUT_YOUR_TOKEN_HERE"
CHAT_ID = "-1003949682698"
PAGE_URL = "https://www.facebook.com/PrayerTimesForKirkuk/"

last_image = ""

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_latest_image():
    try:
        r = requests.get(PAGE_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        images = soup.find_all("img")

        for img in images:
            src = img.get("src")
            if src and "scontent" in src:
                return src

    except Exception as e:
        print("Fetch error:", e)

    return None


def send_photo(photo):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    data = {
        "chat_id": CHAT_ID,
        "photo": photo
    }
    requests.post(url, data=data)


while True:
    img = get_latest_image()

    if img and img != last_image:
        send_photo(img)
        last_image = img
        print("📩 تم إرسال صورة جديدة")

    time.sleep(60)
