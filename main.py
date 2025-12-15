import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

# ========== ПЕРЕМЕННЫЕ ==========
BOT_TOKEN = "8433006649:AAG-XR-l0s0sjDeQ3Jx3AAPNay5RfP1JzWo"
ADMIN_ID = 5228684263  # ваш Telegram ID

# ========== СЛОВАРЬ ИМЕН И ПОДСКАЗОК ==========
available_names = {
    "Вася": "Любит шоколад",
    "Маша": "Обожает книги",
    "Петя": "Фанат LEGO",
    "Света": "Любит готовить",
    "Коля": "Увлекается робототехникой",
    "Оля": "Коллекционирует фигурки",
    "Никита": "Любит компьютерные игры",
    "Аня": "Фанатка настольных игр"
}

# Словарь для хранения, кто кому достался
assigned_santas = {}

# ========== НАСТРОЙКА БОТА ==========
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ========== ОБРАБОТКА /START ==========
@dp.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id

    # Проверяем, не получил ли пользователь уже Тайного Санту
    if user_id in assigned_santas:
        await message.answer(f"Вы уже получили Тайного Санту для: {assigned_santas[user_id]['name']}")
        return

    if not available_names:
        await message.answer("Все имена уже разыграны! Попробуйте позже.")
        return

    # Рандомно выбираем имя + подсказку
    assigned_name, hint = random.choice(list(available_names.items()))
    del available_names[assigned_name]  # чтобы больше не повторялось

    assigned_santas[user_id] = {"name": assigned_name, "hint": hint}

    # Ответ пользователю
    await message.answer(f"Привет! Твой Тайный Санта для: {assigned_name}\nПодсказка: {hint}")

    # Отправка админу
    try:
        admin_message = f"Пользователь @{message.from_user.username or message.from_user.full_name} ({user_id}) получил: {assigned_name} с подсказкой: {hint}"
        await bot.send_message(ADMIN_ID, admin_message)
    except Exception as e:
        print(f"Не удалось отправить сообщение админу: {e}")


# ========== ЗАПУСК БОТА ==========
async def main():
    try:
        print("Бот запущен...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
