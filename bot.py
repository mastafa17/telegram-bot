@bot.message_handler(content_types=['photo', 'document', 'text'])
def test(message):
    print("TYPE:", message.content_type)
    bot.reply_to(message, message.content_type)
