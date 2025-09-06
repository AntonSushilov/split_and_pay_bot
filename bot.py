import logging
import os
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.enums import ChatType, ContentType
import aiohttp
import asyncio

from config import Config

# Загружаем переменные из .env
BOT_TOKEN = Config.BOT_TOKEN
WEB_APP_FRONTEND_URL = Config.WEB_APP_FRONTEND_URL
BACKEND_API_URL = Config.BACKEND_API_URL
# WEB_APP_FRONTEND_URL="https://splitandpay.serveo.net"


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    """
    Обработчик команды /start.
    Отправляет приветственное сообщение и кнопку для отправки номера телефона.
    """
    welcome_text = (
        f"Привет, {message.from_user.first_name}!\n\n"
        "Я — бот SplitAndPay.\n"
        "Я помогу тебе легко и удобно делить счета и расходы с друзьями, "
        "коллегами или семьёй.\n\n"
        "Что я умею:\n"
        "• создавать общие счета\n"
        "• распределять расходы между участниками\n"
        "Для продолжения работы, пожалуйста, отправь свой номер телефона, "
        "нажав на кнопку ниже."
    )

    # Кнопка для запроса телефона
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Отправить номер телефона",
                            request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(welcome_text, reply_markup=keyboard)


@router.message(Command("contact"))
async def send_contact_button(message: Message) -> None:
    """
    Обработчик команды /contact.
    Отправляет кнопку для отправки номера телефона.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Отправить номер телефона",
                            request_contact=True)]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Нажмите кнопку ниже, чтобы поделиться номером",
        reply_markup=keyboard
    )


@router.message(F.content_type == ContentType.CONTACT)
async def handle_contact(message: Message) -> None:
    """
    Обработчик сообщений с типом CONTENT.CONTACT.
    Обрабатывает полученный контакт пользователя, собирает данные и отправляет их на бэкенд.
    """
    user = message.from_user
    phone = message.contact.phone_number
    # Собираем данные пользователя
    user_data = {
        "tg_id": str(user.id),
        "chat_id": str(message.chat.id),
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": phone
    }
    print(f"Собранные данные пользователя: {user_data}")
    # Отправляем на бэкенд
    async with aiohttp.ClientSession() as session:
        await session.post(BACKEND_API_URL + "/user/add", json=user_data)
    await message.answer(f"Спасибо! Мы получили ваш номер: {phone}",
                         reply_markup=ReplyKeyboardRemove()
                         )


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    """
    Обработчик команды /help.
    Отправляет сообщение с описанием доступных команд.
    """
    help_text = (
        "Вот что я умею:\n"
        "/start — начать работу с ботом\n"
        "/help — показать это сообщение\n"
        "/contact — обновить номер телефона\n\n"
        "Я помогу тебе легко делить счета и расходы с друзьями и семьёй."
    )
    await message.answer(help_text)


@router.message(Command("webapp"))
async def webapp_handler(message: Message) -> None:
    """
    Обработчик команды /webapp.
    Отправляет кнопку для открытия WebApp.
    """
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

    await message.answer(
        "Нажми кнопку, чтобы открыть WebApp:",
        reply_markup=keyboard
    )


async def main() -> None:
    """
    Основная функция для запуска бота.
    """
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    """
    Точка входа в приложение.
    """
    # Включаем логирование, чтобы видеть, что происходит
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")
