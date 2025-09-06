from typing import AsyncGenerator
import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=False)
logging.info(f"Database engine created with URL: {DATABASE_URL}")
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронная зависимость для получения сессии базы данных.
    """
    logging.info("Creating new database session")
    async with AsyncSessionLocal() as session:
        yield session
    logging.info("Database session closed")

