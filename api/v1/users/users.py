from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import models
from database import database
from schemas import schemas

router = APIRouter()

@router.post("/auth", response_model=schemas.UserCreate)
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(database.get_async_session)):
    print("user",user)
    query = select(models.User).where(models.User.tg_id == user.tg_id)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        return existing_user  # или raise HTTPException(...) если хочешь

    # Если нет — создаём нового
    db_user = models.User(**user.model_dump())
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user