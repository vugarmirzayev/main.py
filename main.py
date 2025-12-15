import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

BOT_TOKEN = "ВСТАВЬ_СЮДА_НОВЫЙ_ТОКЕН"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("✅ Я живой. Бот работает.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
