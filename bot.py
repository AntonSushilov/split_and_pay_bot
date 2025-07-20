import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ChatType
import aiohttp
import asyncio
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv(".env", override=True)
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_FRONTEND_URL = os.getenv("WEB_APP_FRONTEND_URL")
BACKEND_API_URL = os.getenv("BACKEND_API_URL")
# WEB_APP_FRONTEND_URL="https://splitandpay.serveo.net"

# Включаем логирование, чтобы видеть, что происходит
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Отправить номер телефона", request_contact=True)]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Нажмите кнопку ниже, чтобы поделиться номером:",
        reply_markup=keyboard
    )

@dp.message(lambda msg: msg.contact is not None)
async def handle_contact(message: types.Message):
    user = message.from_user
    contact = message.contact

    user_data = {
        "tg_id": str(user.id),
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": contact.phone_number
    }

    # Отправка на бэкенд
    async with aiohttp.ClientSession() as session:
        print(BACKEND_API_URL+"/users/auth")
        async with session.post(BACKEND_API_URL+"/users/auth", json=user_data) as response:
            print(response)
            if response.status != 200:
                text = await response.text()
                print(f"Ошибка при отправке пользователя: {response.status} {text}")




async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
