from pydantic import BaseModel, Field, model_validator
from enum import Enum
from typing import ClassVar, Optional
from datetime import datetime


class Bank(str, Enum):
    sber = "Сбер"
    tbank = "Т-банк"


class Role(int, Enum):
    admin = 1
    user = 2


class UserCreate(BaseModel):
    tg_id: str = Field(...,
                        description="Идентификатор пользователя в Telegram")
    username: str = Field(..., description="Username пользователя в Telegram")
    first_name: Optional[str] = Field(
        description="Имя пользователя в Telegram")
    last_name: Optional[str] = Field(
        description="Фамилия пользователя в Telegram")
    phone: Optional[str] = Field(
        default=None, description="Телефон пользователя в Telegram")
    bank: Optional[Bank] = Field(default=None, description="Банк пользователя")
    role: Optional[Role] = Field(description="Роль пользователя в системе")

    model_config = {
        "from_attributes": True
    }
    # tg_id, которым можно разрешать роль admin
    ALLOWED_ADMINS: ClassVar[set[str]] = {"394773958"}

    @model_validator(mode="before")
    @classmethod
    def downgrade_invalid_admin(cls, data):
        # Приведение к словарю
        if not isinstance(data, dict):
            data = data.__dict__ if hasattr(data, "__dict__") else dict(data)

        tg_id = str(data.get("tg_id"))
        
        # Если роль не указана, но tg_id в списке — присваиваем роль admin
        if tg_id in cls.ALLOWED_ADMINS:
            data["role"] = Role.admin.value
        else:
            data["role"] = Role.user.value

        print(data)
        return data
