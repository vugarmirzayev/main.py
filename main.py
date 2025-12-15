import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

# Твои переменные
BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"
ADMIN_ID = 123456789  # Ваш Telegram ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Список подарков
GIFTS = [
    "Маленький набор LEGO",
    "Книга по интересам",
    "Симпатичная кружка"
]

@dp.message()
async def handle_message(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id

    # Выбираем случайный подарок
    gift = random.choice(GIFTS)
    
    # Ответ пользователю
    user_text = f"Привет, {user_name}! 🎁 Твой подарок: {gift} (до 50 AZN)"
    await message.answer(user_text)

    # Отправка админу
    admin_text = f"Пользователь: {user_name} (ID: {user_id}) получил подарок: {gift}"
    await bot.send_message(chat_id=ADMIN_ID, text=admin_text)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
