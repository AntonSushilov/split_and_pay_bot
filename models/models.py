from enum import Enum
from sqlalchemy import Column, String, Integer, Enum as SqlEnum, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import Optional, List
from datetime import datetime, timezone

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

class EventStatus(Enum):
    """
    Перечисление статусов события.
    """
    active = "active"
    cancelled = "cancelled"
    completed = "completed"

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
    created_events = relationship("Event", back_populates="creator")
    invited_to_events = relationship("Event", secondary="event_invitations", back_populates="invited_to_events")

class Event(Base):
    """
    Модель события.
    """
    __tablename__ = "events"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)
    start_time: datetime = Column(DateTime, nullable=False)
    end_time: datetime = Column(DateTime, nullable=False)
    creator_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="created_events")
    invited_users = relationship("User", secondary="event_invitations", back_populates="invited_to_events")
    status: EventStatus = Column(SqlEnum(EventStatus), default=EventStatus.active, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

event_invitations = Table(
    "event_invitations",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
)
