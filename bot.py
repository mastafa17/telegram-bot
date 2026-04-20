@bot.message_handler(content_types=['photo'])
def get_file_id(message):
    file_id = message.photo[-1].file_id
    print("FILE ID:", file_id)
    bot.reply_to(message, file_id)
