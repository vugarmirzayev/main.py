from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import asyncio
import random
import os

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Твой Telegram ID для личных сообщений

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Пример участников: list of dict с username и first_name
participants = [
    {"id": 123456, "username": "user1", "first_name": "Vugar"},
    {"id": 234567, "username": "user2", "first_name": "Aysel"},
    {"id": 345678, "username": "user3", "first_name": "Elvin"},
]

# Перемешиваем участников, чтобы назначить кому дарить подарок
def assign_santa(participants):
    givers = participants[:]
    receivers = participants[:]
    random.shuffle(receivers)
    # Если кто-то достался сам себе, меняем
    for i in range(len(givers)):
        if givers[i]["id"] == receivers[i]["id"]:
            # простая перестановка с соседним
            receivers[i], receivers[(i+1)%len(givers)] = receivers[(i+1)%len(givers)], receivers[i]
    return dict(zip([p["id"] for p in givers], receivers))

assignments = assign_santa(participants)

async def notify_participants():
    for giver_id, receiver in assignments.items():
        # Сообщение участнику
        await bot.send_message(giver_id,
            f"Привет! Ты даришь подарок: 🎁 для {receiver['first_name']}"
        )

    # Сообщение админу
    admin_text = "Полный список участников:\n\n"
    for giver_id, receiver in assignments.items():
        giver = next(p for p in participants if p["id"] == giver_id)
        admin_text += f"{giver['username']} -> {receiver['username']}\n"
    await bot.send_message(ADMIN_ID, admin_text)

if __name__ == "__main__":
    asyncio.run(notify_participants())
