import os
import telebot
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

print("BOT STARTED")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    print("FILE ID:", file_id)
    bot.send_message(message.chat.id, file_id)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK"

@app.route("/")
def home():
    return "BOT IS RUNNING"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://YOUR-RAILWAY-URL/{TOKEN}")
    app.run(host="0.0.0.0", port=8080)
