import os
import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InputFile
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from image import process_image
from matematic import determine_and_solve
from database import insert_report, engine
from sympy import latex
from sqlalchemy.exc import SQLAlchemyError
from aiogram.types import FSInputFile
from generate_answer_on_image import process_math_expression

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Конфигурация
TOKEN = "7790375344:AAFM-T2hGdQvzCPmvsOBhj82S5DRIcJfywY"
IMAGE_DIR = "example_images"
ANSWER_IMAGE_DIR = "image_answer_photo"
ABS_PUTH ='C:/python/kur/'
processing_lock = asyncio.Lock()

# Состояния бота
class UserState(StatesGroup):
    waiting_for_math_expression = State()
    waiting_for_report = State()

# Инициализация бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Создаем папки для изображений, если их нет
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(ANSWER_IMAGE_DIR, exist_ok=True)

# Клавиатура с основными командами
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/help"), KeyboardButton(text="/solve")],
            [KeyboardButton(text="/report"), KeyboardButton(text="/examples")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )

async def save_report_to_db(user_id: int, text: str) -> bool:
    try:
        insert_report(user_id, text, engine)
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    welcome_text = """
<b>Добро пожаловать в Math Solver Bot!</b> 

Я помогу вам решить математические задачи:
- По фото 📸
- По тексту 📝

🔹 <b>Основные команды:</b>
/solve - решить текстовый пример
/help - справка по использованию
/report - сообщить об ошибке
"""
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@dp.message(Command("help"))
async def help_command(message: Message, state: FSMContext):
    await state.clear()
    help_text = """
📚 <b>Справка по использованию бота:</b>

<b>1. Решение по фото:</b>
Отправьте четкое фото математического примера

<b>2. Решение текстовых примеров:</b>
Используйте команду /solve

<b>3. Формат текстовых запросов:</b>
- Уравнения: x^2 - 4 = 0
- Интегралы: Integral(x^2, x)
- Производные: diff(sin(x))
- Пределы: Limit(sin(x)/x, x, 0)
- Логарифмы: log(x, 2)

Подробные примеры: /examples
"""
    await message.answer(help_text)

@dp.message(Command("examples"))
async def examples_command(message: Message, state: FSMContext):
    await state.clear()
    examples_text = """
📖 <b>Примеры текстовых запросов</b>

<code>2 + 2 * 2</code> - простые вычисления
<code>x^2 - 4 = 0</code> - уравнение
<code>Integral(x^2, x)</code> - интеграл
<code>diff(sin(x))</code> - производная
<code>Limit(sin(x)/x, x, 0)</code> - предел
<code>log(8, 2)</code> - логарифм
"""
    await message.answer(examples_text)

@dp.message(Command("solve"))
async def solve_command(message: Message, state: FSMContext):
    await state.set_state(UserState.waiting_for_math_expression)
    solve_text = """
🧮 <b>Отправьте математическое выражение для решения</b>

Примеры:
<code>2 + 2 * 2</code>
<code>x^2 - 4 = 0</code>
<code>Integral(x^2, x)</code>
<code>diff(sin(x))</code>

Подробнее: /examples

❌ Чтобы отменить, отправьте /cancel
"""
    await message.answer(solve_text)

@dp.message(Command("report"))
async def report_command(message: Message, state: FSMContext):
    await state.set_state(UserState.waiting_for_report)
    await message.answer("✍️ Пожалуйста, опишите проблему:\n\n❌ Чтобы отменить, отправьте /cancel")

@dp.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Действие отменено", reply_markup=get_main_keyboard())

@dp.message(StateFilter(UserState.waiting_for_report))
async def handle_report(message: Message, state: FSMContext):
    try:
        success = await save_report_to_db(message.from_user.id, message.text)
        if success:
            await state.clear()
            await message.answer("✅ Ваша жалоба успешно сохранена!", reply_markup=get_main_keyboard())
        else:
            await message.answer("⚠️ Не удалось сохранить жалобу. Пожалуйста, попробуйте позже.")
    except Exception as e:
        logger.error(f"Error in handle_report: {e}")
        await message.answer("⚠️ Произошла ошибка при обработке вашей жалобы.")
    finally:
        await state.clear()

@dp.message(StateFilter(UserState.waiting_for_math_expression))
async def handle_math_expression(message: Message, state: FSMContext):
    try:
        expression = message.text.strip()
        await message.answer("🧮 Решаю пример...")
        solution_photo = process_math_expression(expression) 

        image_path = os.path.join(solution_photo)  # Предполагаем, что solution содержит полный путь
        photo = FSInputFile(image_path)
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
            
            # Удаляем временные файлы
        try:
            os.remove(image_path)   # Удаляем обработанный результат
            print(f"Удалены временные файлы: {image_path}")
        except Exception as delete_error:
            logger.error(f"Error deleting temp files: {delete_error}")
            
    except Exception as e:
        logger.error(f"Error processing photo: {e}", exc_info=True)
        await message.answer("⚠️ Произошла ошибка")




@dp.message(lambda message: message.photo)
async def handle_photo(message: Message):
    async with processing_lock:  
        try:
            # Создаем директорию для изображений, если её нет
            os.makedirs(IMAGE_DIR, exist_ok=True)
            
            # Получаем фото максимального качества
            photo = message.photo[-1]
            file_info = await bot.get_file(photo.file_id)

            # Генерируем уникальное имя файла
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            local_path = os.path.join(IMAGE_DIR, f"math_{timestamp}.jpg")

            # Скачиваем файл
            await bot.download_file(file_info.file_path, local_path)
            await message.answer("🔍 Обрабатываю изображение...")
            
            # Обрабатываем изображение
            solution = process_image(local_path)
            print("=================")
            print(local_path)
            print(solution)
            print("=================")

            # Отправляем результат
            image_path = os.path.join(solution)  # Предполагаем, что solution содержит полный путь
            photo = FSInputFile(image_path)
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
            
            # Удаляем временные файлы
            try:
                os.remove(local_path)  # Удаляем скачанное фото
                os.remove(image_path)   # Удаляем обработанный результат
                print(f"Удалены временные файлы: {local_path}, {image_path}")
            except Exception as delete_error:
                logger.error(f"Error deleting temp files: {delete_error}")
            
        except Exception as e:
            logger.error(f"Error processing photo: {e}", exc_info=True)
            await message.answer("⚠️ Произошла ошибка при обработке фото. Попробуйте еще раз.")

       

@dp.message(F.text & ~F.text.startswith('/'))
async def handle_text(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("ℹ️ Пожалуйста, используйте команды из меню или отправьте фото с примером", reply_markup=get_main_keyboard())

async def main():
    logger.info("Starting bot...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())