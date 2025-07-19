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
    tg_id: str = Field(..., description="Идентификатор пользователя в Telegram")
    username: str = Field(..., description="Username пользователя в Telegram")
    first_name: Optional[str] = Field(..., description="Имя пользователя в Telegram")
    last_name: Optional[str] = Field(..., description="Фамилия пользователя в Telegram")
    phone: Optional[str] = Field(default=None, description="Телефон пользователя в Telegram")
    bank: Optional[Bank] = Field(description="Банк пользователя")
    role: Role = Field(default=Role.user, description="Роль пользователя в системе", alias="user_role")

    model_config = {
        "from_attributes": True
    }
    # tg_id, которым можно разрешать роль admin
    ALLOWED_ADMINS: ClassVar[set[str]] = {"394773958"}

    @model_validator(mode="before")
    @classmethod
    def downgrade_invalid_admin(cls, data: dict):
        # Если роль admin и tg_id не разрешён — понижаем до user
        if data.get("role") == Role.admin:
            tg_id = data.get("tg_id")
            if tg_id not in cls.ALLOWED_ADMINS:
                data["role"] = Role.user
        return data