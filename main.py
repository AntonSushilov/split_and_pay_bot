import uvicorn
from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from models import models
from database import database
from api.v1 import v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ⏳ Запуск при старте
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

origins = [
"*"
]

# Подключаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Разрешённые источники
    allow_credentials=True,       # Разрешить куки
    allow_methods=["*"],           # Разрешить все методы (GET, POST, OPTIONS и т.д.)
    allow_headers=["*"],           # Разрешить все заголовки
)


app.include_router(v1_router.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
