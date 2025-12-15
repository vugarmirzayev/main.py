import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio

# ==== ПЕРЕМЕННЫЕ ====
BOT_TOKEN = "8433006649:AAGGiedVbX8DLpr3C5dtTRDHotBZJoybFA0"
ADMIN_ID = 5228684263  # Ваш Telegram ID

# ==== СПИСОК УЧАСТНИКОВ ====
participants = {
    "@shalala_abd": "Parfum, Kosmetika, Ukrashenie No estestvenno lyuboy podarok kotoriy podaren ot dushi samiy lucshiy❤️",
    "@zohra_sultanova": "Красивый букет цветов, духи «Скандал», Новогодний бокс",
    "@nanhasanli": "Плед, мягкие тапочки(39-40) или что-то для уюта",
    "@vugar_mirzayev": "Тут интересно получить что-то по твоей фантазии, первое что пришло в голову прочитав это :) Если совсем не сможешь придумать что-то, можно настольную игру (желательно на русском)",
    "@krb_va": "1)Подарочный купон из Оливия \n2) зимний шарфик ( белого или красного цвета ) только плиз чтобы качество пис олмасын🥺\n3) можно красивую сумочку",
    "@diinmustdie": "Проводные наушники епл ( тайпси , старых нет)\nЭнзимная пудра Anua \nЛосьоны/ баттеры для тела от The Act",
    "@SuzannaBabayeva": "Kiko, parfume, na svoy vibor",
    "@fqrbnv": "Что-то интересное, на ваш вкус",
    "@nika_m_02": "Rare beauty rumana, krasiviy serebrannig brasletik ili kolco, bolshoy sharf (ctobi tuku tokulmesin) beliy ili bordovoy, nudovaya pomada ot anastasiya. Odin iz nix no glavnoye vnimaniye❤️😂 Cox sagolun))",
    "@Geydarova98": "Подарок, выбранный с вниманием и теплом ☃️",
    "@farakhhh": "Вещь, которая всегда останется в памяти. Что-то ароматное🥰",
    "@Nara_Vn": "На свой вкус 😁",
    "@taqievelnur": "Elektrik dish shetkasi, Masa uchun hediyye suvenirchik, La Roche - Posay (uz penkasi fake olmasin pls uzum hessasdi) Ve ya konlunuzden ne kecirse onuda ala bilersiniz✨"
}

# ==== БОТ И ДИСПАТЧЕР ====
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ==== КОМАНДА /start ====
@dp.message(Command(commands=["start"]))
async def start_santa(message: Message):
    user_username = f"@{message.from_user.username}" if message.from_user.username else None

    if not user_username or user_username not in participants:
        await message.answer("Вы не зарегистрированы в Secret Santa списке.")
        return

    # Исключаем самого себя
    available = {k: v for k, v in participants.items() if k != user_username}

    if not available:
        await message.answer("Пока нет доступных участников для жеребьёвки.")
        return

    # Выбор случайного участника
    santa, hint = random.choice(list(available.items()))

    # Отправляем пользователю его "сантa"
    await message.answer(f"🎁 Ваш Secret Santa: {santa}\n💡 Подсказка: {hint}")

    # Отправляем администратору
    await bot.send_message(ADMIN_ID, f"{user_username} получил {santa} с подсказкой:\n{hint}")

# ==== ЗАПУСК БОТА ====
if __name__ == "__main__":
    import asyncio
    from aiogram import F
    from aiogram.utils import exceptions

    async def main():
        try:
            await dp.start_polling(bot)
        except exceptions.TelegramAPIError as e:
            print(f"Ошибка Telegram API: {e}")

    asyncio.run(main())
