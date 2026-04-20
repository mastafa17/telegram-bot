from aiogram import F

# هذا الكود مخصص فقط لاستخراج الـ IDs
@dp.message(F.photo)
async def get_photo_id(message: types.Message):
    # نأخذ آخر صورة (تكون بأعلى دقة)
    photo_id = message.photo[-1].file_id
    await message.answer(f"كود الصورة (File ID) هو:\n\n`{photo_id}`", parse_mode="MarkdownV2")
