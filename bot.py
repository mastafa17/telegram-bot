import asyncio
import os
from aiogram import Bot, Dispatcher, F, types

# ضع التوكن الخاص بك هنا مؤقتاً للتجربة
API_TOKEN = "ضع_توكن_بوتك_هنا"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(F.photo)
async def handle_photos(message: types.Message):
    # الحصول على ID الصورة بدقة عالية
    file_id = message.photo[-1].file_id
    await message.reply(f"وصلت الصورة بنجاح! ✅\n\nالـ ID الخاص بها هو:\n`{file_id}`", parse_mode="Markdown")

@dp.message()
async def any_message(message: types.Message):
    await message.reply("أرسل لي صورة (Photo) وليس ملفاً لكي أعطيك الـ ID.")

async def main():
    print("البوت يعمل الآن.. أرسل الصور إليه للحصول على الـ ID")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
