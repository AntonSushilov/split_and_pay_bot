import uvicorn
from fastapi import FastAPI, APIRouter, Depends
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from models import models
from database import database
from schemas import schemas
from api.v1 import users as users_v1

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ⏳ Запуск при старте
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users_v1.router, prefix="/api/v1/users")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
