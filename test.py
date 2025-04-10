TOKEN = "7790375344:AAFM-T2hGdQvzCPmvsOBhj82S5DRIcJfywY"

import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile  # Изменили InputFile на FSInputFile
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Путь к папке с изображениями
IMAGE_FOLDER = "example_images"
dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

@dp.message(Command("pic"))
async def send_image(message: types.Message):
    image_name = "math_013a82651652465bb11a4dd90231786d.png"
    image_path = os.path.join(IMAGE_FOLDER, image_name)

    if not os.path.exists(image_path):
        await message.reply("Изображение не найдено! 😢")
        return

    # Используем FSInputFile вместо InputFile
    photo = FSInputFile(image_path)
    await bot.send_photo(chat_id=message.chat.id, photo=photo)

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())