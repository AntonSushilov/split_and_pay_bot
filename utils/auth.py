from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from database import database
from utils.hash_webbapp import validate_telegram_webapp_hash, parse_webapp_init_data

async def get_current_user(init_data: str, bot_token: str, session: AsyncSession = Depends(database.get_async_session)):
    try:
        parsed_data = parse_webapp_init_data(bot_token, init_data)
        user_id = parsed_data['user']['id']
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user