@dp.message(F.photo)
async def get_photo_id(message: types.Message):
    # هذا السطر سيعطيك الـ ID الخاص بالصورة
    await message.answer(f"ID الصورة هو:\n`{message.photo[-1].file_id}`", parse_mode="MarkdownV2")
