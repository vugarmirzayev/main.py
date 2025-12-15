import os
import random
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 🔧 УКАЖИ УЧАСТНИКОВ И ПОДСКАЗКИ
participants = {
    "Али": "Любит кофе",
    "Мария": "Обожает сладкое",
    "Илья": "Фанат техники",
    "Анна": "Любит уют и свечи",
}

assigned = {}   # user_id -> (имя, подсказка)
available = list(participants.keys())


@dp.message()
async def start_handler(message: Message):
    if message.text != "/start":
        return

    user_id = message.from_user.id

    # Если уже получал — показываем снова
    if user_id in assigned:
        name, hint = assigned[user_id]
        await message.answer(
            f"🎅 *Твой Secret Santa*\n\n"
            f"*{name}*\n"
            f"Подсказка: {hint}",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if not available:
        await message.answer("🎄 Все участники уже распределены")
        return

    chosen = random.choice(available)
    available.remove(chosen)

    assigned[user_id] = (chosen, participants[chosen])

    await message.answer(
        f"🎁 *Твой Secret Santa*\n\n"
        f"*{chosen}*\n"
        f"Подсказка: {participants[chosen]}",
        parse_mode=ParseMode.MARKDOWN
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
