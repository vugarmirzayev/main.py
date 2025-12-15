import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import executor

API_TOKEN = os.getenv("BOT_TOKEN")  # ваш токен
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # ваш Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Form(StatesGroup):
    waiting_for_name = State()

# Старт
@dp.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        "Привет! Как тебя зовут?",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Form.waiting_for_name)

# Получение имени
@dp.message(Form.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    user_name = message.text
    user_id = message.from_user.id

    # Ответ участнику
    await message.answer(f"Приятно познакомиться, {user_name}! ✅")

    # Уведомление админа
    await bot.send_message(
        ADMIN_ID,
        f"Новый участник:\nИмя: {user_name}\nID: {user_id}"
    )

    await state.clear()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
