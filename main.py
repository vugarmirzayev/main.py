import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

API_TOKEN = "ВАШ_ТОКЕН_БОТА"
ADMIN_ID = 5228684263  # Ваш Telegram ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Словарь "подарки"
GIFTS = [
    "Маленький набор LEGO",
    "Книга по интересам",
    "Симпатичная кружка"
]

@dp.message()
async def santa_reply(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id

    # Выбираем подарок случайным образом
    import random
    gift = random.choice(GIFTS)
    
    # Ответ пользователю
    user_text = f"Привет, {user_name}! 🎁 Твой подарок: {gift} (до 50 AZN)"
    await message.answer(user_text)

    # Отправляем админу
    admin_text = f"Пользователь: {user_name} (ID: {user_id}) получил подарок: {gift}"
    await bot.send_message(chat_id=ADMIN_ID, text=admin_text)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
