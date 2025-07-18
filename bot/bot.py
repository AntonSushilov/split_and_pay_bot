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
load_dotenv(".env")
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_FRONTEND_URL = os.getenv("WEB_APP_FRONTEND_URL")
# WEB_APP_FRONTEND_URL="https://splitandpay.serveo.net"

# Включаем логирование, чтобы видеть, что происходит
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

@dp.message(Command('start'))
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть WebApp",
                    web_app=WebAppInfo(url=WEB_APP_FRONTEND_URL)
                )
            ]
        ]
    )
    # keyboard = ReplyKeyboardMarkup(
    #     keyboard=[
    #         [KeyboardButton(text="Открыть WebApp", web_app=WebAppInfo(url=WEB_APP_FRONTEND_URL))]
    #     ],
    #     resize_keyboard=True
    # )
    await message.answer("Нажми кнопку, чтобы открыть WebApp:", reply_markup=keyboard)

@dp.message(Command("contact"))
async def send_contact_button(message: Message):
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

@dp.message(F.content_type == "contact")
async def handle_contact(message: Message):
    phone = message.contact.phone_number
    await message.answer(f"Спасибо! Мы получили ваш номер: {phone}")



async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
