from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from utils import validate_telegram_webapp_hash, parse_webapp_init_data
from models import models
from database import database
from schemas import AuthRequest, DataResponse, UserCreate
from config import Config
router = APIRouter()

BOT_TOKEN = Config.BOT_TOKEN

@router.post("/add", response_model=DataResponse[UserCreate])
async def create_user(user: UserCreate, session: AsyncSession = Depends(database.get_async_session)):
    query = select(models.User).where(models.User.tg_id == user.tg_id)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()
    print("*" * 20)
    print(f"Проверка существования пользователя: {existing_user}")
    if existing_user:
        return {
            "status": "success",
            "data": UserCreate.model_validate(existing_user),
            "message": "Пользователь уже существует.",
        }  # или raise HTTPException(...) если хочешь

    # Если нет — создаём нового
    db_user = models.User(**user.model_dump())
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return {
        "status": "success",
        "data": db_user,
        "message": "Пользователь успешно создан."}


@router.post("/edit", response_model=DataResponse[UserCreate])
async def edit_user(user: UserCreate, session: AsyncSession = Depends(database.get_async_session)):
    query = select(models.User).where(models.User.tg_id == user.tg_id)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        return {
            "status": "error",
            "data": None,
            "message": "Пользователь не найден."
        }

    for key, value in user.model_dump().items():
        setattr(existing_user, key, value)

    await session.commit()
    await session.refresh(existing_user)

    return {
        "status": "success",
        "data": UserCreate.model_validate(existing_user),
        "message": "Пользователь успешно обновлён."
    }


@router.post("/auth", response_model=DataResponse[UserCreate])
async def auth_user(initData: AuthRequest, session: AsyncSession = Depends(database.get_async_session)):
    check = validate_telegram_webapp_hash(BOT_TOKEN, initData.initData)
    if not check:
        return {
            "status": "error",
            "data": None,
            "message": "Неверная подпись веб-приложения."
        }
    parseInitData = parse_webapp_init_data(BOT_TOKEN, initData.initData)
    query = select(models.User).where(models.User.tg_id == parseInitData.user.id)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        return {
            "status": "error",
            "data": None,
            "message": "Пользователь не найден."
        }

    return {
        "status": "success",
        "data": UserCreate.model_validate(existing_user),
        "message": "Пользователь успешно авторизован."
    }