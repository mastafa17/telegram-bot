import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

TOKEN = "8559357103:AAGTeH5u4DiwDYZDBSDn4z1O7P3pBXwDse4"
CHAT_ID = "-1003949682698"
PAGE_URL = "https://www.facebook.com/PrayerTimesForKirkuk/"

last_image = ""

driver = webdriver.Chrome()

def get_latest_image():
    driver.get(PAGE_URL)
    time.sleep(6)

    # نركز على صور المنشورات فقط
    images = driver.find_elements(By.XPATH, "//div[contains(@class,'x1yztbdb')]//img")

    for img in images:
        src = img.get_attribute("src")
        if src and "scontent" in src:
            return src

    return None

def send_photo(photo):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    data = {
        "chat_id": CHAT_ID,
        "photo": photo
    }
    requests.post(url, data=data)

while True:
    try:
        img = get_latest_image()

        if img and img != last_image:
            send_photo(img)
            last_image = img
            print("📩 تم إرسال صورة جديدة")

    except Exception as e:
        print("خطأ:", e)

    time.sleep(60)