import os
import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from image import process_image
from matemaric import determine_and_solve

processing_lock = asyncio.Lock()

TOKEN = "7790375344:AAFM-T2hGdQvzCPmvsOBhj82S5DRIcJfywY"
IMAGE_DIR = "example_image"

def process_image1(image_path):
    return process_image(image_path)

def generate_response(solution):
    if not isinstance(solution, str):  
        solution = str(solution)  # Преобразуем SymPy-объект в строку
    solution1 = determine_and_solve(solution)
    return f"Вот ответ: <b>{solution1}</b>"


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Скинь фото примера")

@dp.message(lambda message: message.photo)
async def handle_photo(message: Message):
    async with processing_lock:  
        os.makedirs(IMAGE_DIR, exist_ok=True)

        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  
        local_path = os.path.join(IMAGE_DIR, f"b1_{timestamp}.jpg")

        await bot.download_file(file_info.file_path, local_path)
      
        solution = process_image1(local_path)
        response = generate_response(solution)

        await message.answer(response)

        os.remove(local_path)

async def main():
    await dp.start_polling(bot)

if __name__  == "__main__":
    asyncio.run(main())