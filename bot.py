@bot.message_handler(func=lambda m: True)
def test(message):
    print("MESSAGE TYPE:", message.content_type)
    bot.reply_to(message, "OK")
