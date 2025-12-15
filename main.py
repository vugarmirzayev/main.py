import asyncio
import random
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

# ================== НАСТРОЙКИ ==================

BOT_TOKEN = "8433006649:AAGGiedVbX8DLpr3C5dtTRDHotBZJoybFA0"
ADMIN_ID = 5228684263  # твой Telegram ID (числом)

# ================== ДАННЫЕ САНТЫ ==================

available_names = {
    "Shalala Abdullayeva": "Parfum, Kosmetika, Ukrashenie. Lyuboy podarok ot dushi — samiy luchshiy ❤️",

    "Zohra Sultanova": "Красивый букет цветов, духи «Скандал», новогодний бокс",

    "Narmin Hasanli": "Плед, мягкие тапочки (39–40) или что-то для уюта",

    "Vugar Mirzayev": """Что-то по твоей фантазии 🙂
Если сложно — настольная игра (желательно на русском)""",

    "Amina Qarabayova": """Подарочный купон Olivia
Зимний шарфик (белый или красный)
Красивая сумочка""",

    "Diana Babayeva": """Проводные наушники Apple (Type-C)
Энзимная пудра Anua
Лосьоны / баттеры The Act""",

    "Suzanna Babayeva": "Kiko, parfum — на свой выбор",

    "Farid Gurbanov": "Что-то интересное, на ваш вкус",

    "Nigar Mustafayeva": """Rare Beauty румяна
Серебряный браслет или кольцо
Большой шарф
Нюдовая помада Anastasia""",

    "Malaknisa Heydarzada": "Подарок с вниманием и теплом ☃️",

    "Farah Hazizada": "Что-то ароматное и запоминающееся 🥰",

    "Nargiz Valizada": "На свой вкус 😁",

    "Elnur Tagiyev": """Электрическая зубная щётка
Сувенир для стола
La Roche-Posay (не фейк)
Или что угодно от души ✨"""
}

# ================== ИНИЦИАЛИЗАЦИЯ ==================

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ================== ОБРАБОТЧИК ==================

@dp.message(CommandStart())
async def start(message: Message):
    global available_names

    if not available_names:
        await message.answer("🎄 Все участники уже распределены. Спасибо!")
        return

    # случайный выбор
    name = random.choice(list(available_names.keys()))
    hint = available_names.pop(name)

    # сообщение участнику
    await message.answer(
        f"🎅 Твой Secret Santa:\n\n"
        f"👤 {name}\n\n"
        f"🎁 Подсказка:\n{hint}"
    )

    # сообщение админу
    sender = message.from_user
    sender_name = sender.full_name
    sender_username = f"@{sender.username}" if sender.username else "без username"

    await bot.send_message(
        ADMIN_ID,
        f"📬 Новый участник\n\n"
        f"От: {sender_name} ({sender_username})\n"
        f"Выпал: {name}"
    )

# ================== ЗАПУСК ==================

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
