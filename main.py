import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F

# --- ПЕРЕМЕННЫЕ (можно задать прямо здесь) ---
BOT_TOKEN = os.getenv("BOT_TOKEN") or "8433006649:AAG-XR-l0s0sjDeQ3Jx3AAPNay5RfP1JzWo"
ADMIN_ID = int(os.getenv("ADMIN_ID") or 5228684263)  # замените на свой Telegram ID

# Проверка токена
if not BOT_TOKEN or BOT_TOKEN == "ВАШ_ТОКЕН_БОТА_СЮДА":
    raise ValueError("Установите корректный BOT_TOKEN!")

if not ADMIN_ID or ADMIN_ID == 123456789:
    raise ValueError("Установите корректный ADMIN_ID!")

# --- Создаем бота и диспетчер ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Обработка команды /start ---
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я бот.")

    # Отправляем админу информацию о том, кто стартанул
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Пользователь @{message.from_user.username} ({message.from_user.id}) нажал /start."
    )

# --- Обработка текстовых сообщений ---
@dp.message(F.text)
async def echo_handler(message: Message):
    await message.answer(f"Вы написали: {message.text}")

    # Отправляем админу копию сообщения
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Сообщение от @{message.from_user.username} ({message.from_user.id}): {message.text}"
    )

# --- Запуск бота ---
async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
