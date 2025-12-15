import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import executor

# -------------------- Настройки --------------------
API_TOKEN = os.getenv("BOT_TOKEN")   # Токен бота
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Твой Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# -------------------- FSM --------------------
class Form(StatesGroup):
    waiting_for_name = State()

# -------------------- Клавиатура --------------------
def get_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="Отправить имя"))
    return kb.as_markup(resize_keyboard=True)

# -------------------- Хэндлеры --------------------
@dp.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        "Привет! Как тебя зовут?",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(Form.waiting_for_name)

@dp.message(Form.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    user_name = message.text
    user_id = message.from_user.id

    # Отправляем участнику ответ
    await message.answer(f"Приятно познакомиться, {user_name}! ✅")

    # Отправляем уведомление админу
    await bot.send_message(
        ADMIN_ID,
        f"Новый участник:\nИмя: {user_name}\nID: {user_id}"
    )

    # Завершаем FSM
    await state.clear()

# -------------------- Запуск --------------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
