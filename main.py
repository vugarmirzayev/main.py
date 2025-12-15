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
    "Shalala Abdullayeva": "Parfum, Kosmetika, Ukrashenie No estestvenno lyuboy podarok kotoriy podaren ot dushi samiy lucshiy❤️",
    "Zohra Sultanova": "Красивый букет цветов, духи «Скандал», Новогодний бокс",
    "Narmin Hasanli": "Плед, мягкие тапочки(39-40) или что-то для уюта",
    "Vugar Mirzayev": "Тут интересно получить что-то по твоей фантазии, первое что пришло в голову прочитав это :)
Если совсем не сможешь придумать что то, можно настольную игру (желательно на русском)",
    "Amina Qarabayova": "1)Подарочный купон из Оливия 
2) зимний шарфик ( белого или красного цвета ) только плиз чтобы качество пис олмасын🥺
3) можно красивую сумочку",
    "Diana Babayeva": "Проводные наушники епл ( тайпси , старых нет)
Энзимная пудра Anua 
Лосьоны/ баттеры для тела от The Act",
    "Suzanna Babayeva": "Kiko, parfume, na svoy vibor",
    "Farid Gurbanov": "Что то интересное, на ваш вкус",
    "Nigar Mustafayeva": "Rare beauty rumana, krasiviy serebrannig brasletik ili kolco, bolshoy sharf (ctobi tuku tokulmesin) beliy ili bordovoy, nudovaya pomada ot anastasiya. 
Odin iz nix no glavnoye vnimaniye❤️😂 Cox sagolun))",
"Malaknisa Heydarzada": "Подарок, выбранный с вниманием и теплом ☃️",
"Farah Hazizada": "Вещь, которая всегда останется в памяти.
Что-то ароматное🥰",
    "Nargiz Valizada": "На свой вкус 😁",
    "Elnur Tagiyev": "Elektrik dish shetkasi, Masa uchun hediyye suvenirchik, La Roche - Posay (uz penkasi fake olmasin pls uzum hessasdi) 
Ve ya konlunuzden ne kecirse onuda ala bilersiniz✨"
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
