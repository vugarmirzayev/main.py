import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"
ADMIN_ID = 123456789  # ваш Telegram ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Список участников (user_id: full_name)
participants = {}

# Список уже назначенных подарков (user_id: user_id кому дарит)
assigned = {}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    # Добавляем пользователя в список участников
    participants[user_id] = full_name

    await message.answer(f"Привет, {full_name}! Вы зарегистрированы для игры 'Случайный Санта'.\n"
                         "Когда все будут готовы, напишите /get_santa, чтобы узнать, кому вы дарите подарок.")
    
    # Отправляем администратору уведомление
    await bot.send_message(ADMIN_ID, f"Новый участник: {full_name} ({user_id})")

@dp.message(Command("get_santa"))
async def get_santa_handler(message: types.Message):
    user_id = message.from_user.id

    if user_id not in participants:
        await message.answer("Сначала нужно зарегистрироваться через /start")
        return

    # Проверяем, что пользователь еще не получил подарок
    if user_id in assigned:
        santa_id = assigned[user_id]
        santa_name = participants[santa_id]
        await message.answer(f"Вы уже получили подарок для: {santa_name}")
        return

    # Формируем список доступных для назначения (не самого себя и тех, кто уже назначен)
    available = [uid for uid in participants.keys() if uid != user_id and uid not in assigned.values()]
    
    if not available:
        await message.answer("К сожалению, пока нет доступных участников для назначения.")
        return

    # Случайный выбор
    chosen_id = random.choice(available)
    assigned[user_id] = chosen_id
    chosen_name = participants[chosen_id]

    # Отправляем пользователю результат
    await message.answer(f"Вы дарите подарок: {chosen_name}")

    # Отправляем администратору уведомление
    await bot.send_message(ADMIN_ID, f"{participants[user_id]} ({user_id}) дарит подарок {chosen_name} ({chosen_id})")

async def main():
    try:
        print("Бот запущен...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
