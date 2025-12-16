import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

# ==== ПЕРЕМЕННЫЕ ====
BOT_TOKEN = "8433006649:AAGGiedVbX8DLpr3C5dtTRDHotBZJoybFA0"
ADMIN_ID = 5228684263  # Ваш Telegram ID

# ==== СПИСОК УЧАСТНИКОВ ====
participants = {
    
    "@nanhasanli": "Плед, мягкие тапочки(39-40) или что-то для уюта",
    "@EmilKichibeyov": "Футбольная форма"
}

# ==== СЛОВАРЬ ДЛЯ УЖЕ РАЗДАННЫХ САНТ ====
assigned = {}  # user_username -> santa_username

# ==== БОТ И ДИСПАТЧЕР ====
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ==== КОМАНДА /start ====
@dp.message(Command(commands=["start"]))
async def start_santa(message: types.Message):
    user_username_raw = message.from_user.username
    if not user_username_raw:
        await message.answer("У вас нет username в Telegram. Пожалуйста, добавьте его и попробуйте снова.")
        return

    user_username = f"@{user_username_raw}"

    if user_username not in participants:
        await message.answer("Вы не зарегистрированы в Secret Santa списке.")
        return

    if user_username in assigned:
        santa_username = assigned[user_username]
        hint = participants[santa_username]
        await message.answer(f"🎁 Ваш Secret Santa уже выбран: {santa_username}\n💡 Подсказка: {hint}")
        return

    # Доступные участники: исключаем самого себя и уже разыгранных
    available = [u for u in participants.keys() if u != user_username and u not in assigned.values()]

    if not available:
        await message.answer("Пока нет доступных участников для жеребьёвки.")
        return

    # Выбор случайного участника
    santa_username = random.choice(available)
    hint = participants[santa_username]

    # Сохраняем результат
    assigned[user_username] = santa_username

    # Отправляем пользователю
    await message.answer(f"🎁 Ваш Secret Santa: {santa_username}\n💡 Подсказка: {hint}")

    # Отправляем администратору
    await bot.send_message(ADMIN_ID, f"{user_username} получил {santa_username} с подсказкой:\n{hint}")

# ==== ЗАПУСК БОТА ====
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
