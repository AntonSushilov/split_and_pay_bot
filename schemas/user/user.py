from pydantic import BaseModel, Field, model_validator
from typing import ClassVar, Optional

from schemas import Role, Bank


class UserCreate(BaseModel):
    tg_id: str = Field(...,
                       description="Идентификатор пользователя в Telegram")
    chat_id: str = Field(..., description="Идентификатор чата в Telegram")
    username: str = Field(..., description="Username пользователя в Telegram")
    first_name: Optional[str] = Field(...,
                                      description="Имя пользователя в Telegram")
    last_name: Optional[str] = Field(...,
                                     description="Фамилия пользователя в Telegram")
    phone: Optional[str] = Field(
        default=None, description="Телефон пользователя в Telegram")
    bank: Optional[Bank] = Field(default=None, description="Банк пользователя")
    role: Role = Field(
        default=Role.user, description="Роль пользователя в системе")

    # tg_id, которым можно разрешать роль admin
    ALLOWED_ADMINS: ClassVar[set[str]] = {"394773958"}

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    @classmethod
    def downgrade_invalid_admin(cls, data):
        # Унифицируем доступ к данным
        as_dict = data if isinstance(data, dict) else data.__dict__.copy()
        role = as_dict.get("role")
        tg_id = as_dict.get("tg_id")

        # Логика назначения роли
        if str(tg_id) in cls.ALLOWED_ADMINS:
            as_dict["role"] = Role.admin
        elif role == Role.admin:
            as_dict["role"] = Role.user
        # Возвращаем в том же формате, что пришло
        if isinstance(data, dict):
            return as_dict
        for k, v in as_dict.items():
            setattr(data, k, v)
        return data

