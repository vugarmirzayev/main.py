import os
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8433006649:AAG-XR-l0s0sjDeQ3Jx3AAPNay5RfP1JzWo"
ADMIN_ID = int(os.getenv("ADMIN_ID") or 5228684263)  # замените на свой Telegram ID

# Проверка токена
if not BOT_TOKEN or BOT_TOKEN == "ВАШ_ТОКЕН_БОТА_СЮДА":
    raise ValueError("Установите корректный BOT_TOKEN!")

if not ADMIN_ID or ADMIN_ID == 123456789:
    raise ValueError("Установите корректный ADMIN_ID!")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Все имена, которые можно раздать
available_names = [
   "Вася": "Любит шоколад",
    "Маша": "Обожает книги",
    "Петя": "Фанат LEGO",
    "Света": "Любит готовить",
    "Коля": "Увлекается робототехникой",
    "Оля": "Коллекционирует фигурки",
    "Никита": "Любит компьютерные игры",
    "Аня": "Фанатка настольных игр"
]

# Словарь, чтобы отслеживать кому кто достался
assigned_santas = {}

@dp.message(F.text == "/start")
async def start(message: Message):
    user_id = message.from_user.id
    
    if user_id in assigned_santas:
        await message.answer(f"Привет! Ты уже получил имя: {assigned_santas[user_id]}")
        return
    
    if not available_names:
        await message.answer("Извини, имена закончились, больше никому не можем назначить Санту.")
        return

    # Выбираем рандомное имя
    assigned_name = random.choice(available_names)
    available_names.remove(assigned_name)  # чтобы больше не повторялось
    assigned_santas[user_id] = assigned_name

    # Отправляем участнику
    await message.answer(f"Привет! Твой Тайный Санта для: {assigned_name}")
    
    # Отправляем админу
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Пользователь @{message.from_user.username} ({user_id}) — получил {assigned_name}"
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
