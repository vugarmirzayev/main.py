import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# ===== Настройки =====
BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"
ADMIN_ID = 123456789  # ваш Telegram ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ===== Обработчик команды /start =====
@dp.message(Command("start"))
async def start_handler(message: Message):
    user_name = message.from_user.full_name
    # Ответ пользователю
    await message.answer(f"Привет, {user_name}! Я получил твоё сообщение.")
    
    # Уведомление админу
    await bot.send_message(ADMIN_ID, f"Пользователь {user_name} ({message.from_user.id}) написал /start.")

# ===== Обработчик текстовых сообщений =====
@dp.message()
async def text_handler(message: Message):
    user_name = message.from_user.full_name
    user_text = message.text
    
    # Ответ пользователю
    await message.answer(f"Вы написали: {user_text}")
    
    # Уведомление админу
    await bot.send_message(ADMIN_ID, f"Пользователь {user_name} ({message.from_user.id}) написал: {user_text}")

# ===== Запуск бота =====
async def main():
    try:
        print("Бот запущен...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
