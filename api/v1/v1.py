from fastapi import APIRouter
import logging
from typing import Dict

from .users import users

router = APIRouter()

@router.get("/")
async def read_root() -> Dict[str, str]:
    """
    Корневой маршрут API.
    Возвращает приветственное сообщение.
    """
    logging.info("Handling root endpoint")
    return {"message": "Welcome to the SplitAndPay API"}

# Include the users router with a prefix and tags
router.include_router(users.router, prefix="/users", tags=["Users"])