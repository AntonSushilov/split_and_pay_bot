from enum import Enum
from sqlalchemy import Column, String, Integer, Enum as SqlEnum
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional

Base = declarative_base()

class Bank(Enum):
    """
    Перечисление банков.
    """
    sber = "Сбер"
    tbank = "Т-банк"

class Role(Enum):
    """
    Перечисление ролей пользователей.
    """
    admin = 1
    user = 2

class User(Base):
    """
    Модель пользователя.
    """
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    tg_id: str = Column(String, unique=True, index=True, nullable=False)
    chat_id: str = Column(String, unique=True, index=True, nullable=False)
    username: str = Column(String, nullable=False)
    first_name: Optional[str] = Column(String, nullable=True)
    last_name: Optional[str] = Column(String, nullable=True)
    phone: Optional[str] = Column(String, nullable=True)
    bank: Optional[Bank] = Column(SqlEnum(Bank), nullable=True)
    role: Role = Column(SqlEnum(Role), default=Role.user, nullable=False)
