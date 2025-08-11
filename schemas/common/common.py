from enum import Enum
from typing import Generic, TypeVar
from pydantic import BaseModel

class Bank(str, Enum):
    sber = "Сбер"
    tbank = "Т-банк"


class Role(int, Enum):
    admin = 1
    user = 2


# Обозначаем универсальный тип для data
T = TypeVar('T')

# Создаем универсальную схему ответа
class DataResponse(BaseModel, Generic[T]):
    status: str
    data: T
    message: str

class AuthRequest(BaseModel):
    initData: str
