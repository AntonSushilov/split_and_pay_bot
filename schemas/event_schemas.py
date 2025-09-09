from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from models.models import EventStatus

class EventCreate(BaseModel):
    name: str = Field(..., title="Название события", max_length=255)
    description: Optional[str] = Field(None, title="Описание события", max_length=1000)
    start_time: datetime = Field(..., title="Время начала события")
    end_time: datetime = Field(..., title="Время окончания события")
    status: EventStatus = Field(..., title="Статус события")

class EventInvite(BaseModel):
    user_ids: List[int] = Field(..., title="Список ID пользователей для приглашения")

class EventUpdate(BaseModel):
    name: Optional[str] = Field(None, title="Название события", max_length=255)
    description: Optional[str] = Field(None, title="Описание события", max_length=1000)
    start_time: Optional[datetime] = Field(None, title="Время начала события")
    end_time: Optional[datetime] = Field(None, title="Время окончания события")
    status: Optional[EventStatus] = Field(None, title="Статус события")

class EventResponse(BaseModel):
    id: int = Field(..., title="ID события")
    title: str = Field(..., title="Название события")
    description: Optional[str] = Field(None, title="Описание события")
    start_time: datetime = Field(..., title="Время начала события")
    end_time: datetime = Field(..., title="Время окончания события")
    creator_id: int = Field(..., title="ID создателя события")
    status: EventStatus = Field(..., title="Статус события")
    created_at: datetime = Field(..., title="Время создания события")
    updated_at: datetime = Field(..., title="Время последнего обновления события")

    class Config:
        from_attributes = True

class EventsListResponse(BaseModel):
    events: List[EventResponse] = Field(..., title="Список событий")
    total: int = Field(..., title="Общее количество событий")