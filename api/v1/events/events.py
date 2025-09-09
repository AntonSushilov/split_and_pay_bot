from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from typing import List

from utils import get_current_user
from models import models
from database import database
from schemas import event_schemas
from config import Config

router = APIRouter()

@router.post("/create", response_model=event_schemas.EventResponse)
async def create_event(event: event_schemas.EventCreate, session: AsyncSession = Depends(database.get_async_session), current_user: models.User = Depends(get_current_user)):
    db_event = models.Event(**event.model_dump(), creator_id=current_user.id)
    session.add(db_event)
    await session.commit()
    await session.refresh(db_event)
    return db_event

@router.get("/list", response_model=event_schemas.EventsListResponse)
async def get_events(session: AsyncSession = Depends(database.get_async_session)):
    query = select(models.Event)
    result = await session.execute(query)
    events = result.scalars().all()
    return {"events": events, "total": len(events)}

@router.get("/{event_id}", response_model=event_schemas.EventResponse)
async def get_event(event_id: int, session: AsyncSession = Depends(database.get_async_session)):
    query = select(models.Event).where(models.Event.id == event_id)
    result = await session.execute(query)
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    return event

@router.put("/{event_id}", response_model=event_schemas.EventResponse)
async def update_event(event_id: int, event: event_schemas.EventUpdate, session: AsyncSession = Depends(database.get_async_session), current_user: models.User = Depends(get_current_user)):
    query = select(models.Event).where(models.Event.id == event_id)
    result = await session.execute(query)
    db_event = result.scalar_one_or_none()
    if not db_event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    if db_event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на обновление этого события")
    
    for key, value in event.model_dump().items():
        if value is not None:
            setattr(db_event, key, value)
    
    await session.commit()
    await session.refresh(db_event)
    return db_event

@router.delete("/{event_id}", response_model=event_schemas.EventResponse)
async def delete_event(event_id: int, session: AsyncSession = Depends(database.get_async_session), current_user: models.User = Depends(get_current_user)):
    query = select(models.Event).where(models.Event.id == event_id)
    result = await session.execute(query)
    db_event = result.scalar_one_or_none()
    if not db_event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    if db_event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на удаление этого события")
    
    await session.delete(db_event)
    await session.commit()
    return db_event

@router.post("/{event_id}/invite", response_model=event_schemas.EventResponse)
async def invite_user_to_event(event_id: int, invite_data: event_schemas.EventInvite, session: AsyncSession = Depends(database.get_async_session), current_user: models.User = Depends(get_current_user)):
    query = select(models.Event).where(models.Event.id == event_id)
    result = await session.execute(query)
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    if event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на приглашение пользователей на это событие")
    
    for user_id in invite_data.user_ids:
        query = select(models.User).where(models.User.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail=f"Пользователь с ID {user_id} не найден")
        
        await session.execute(insert(models.event_invitations).values(event_id=event_id, user_id=user_id))
    
    await session.commit()
    await session.refresh(event)
    return event

@router.delete("/{event_id}/invite/{user_id}", response_model=event_schemas.EventResponse)
async def cancel_user_invitation(event_id: int, user_id: int, session: AsyncSession = Depends(database.get_async_session), current_user: models.User = Depends(get_current_user)):
    query = select(models.Event).where(models.Event.id == event_id)
    result = await session.execute(query)
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    if event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на отмену приглашения пользователей на это событие")
    
    query = select(models.User).where(models.User.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    await session.execute(delete(models.event_invitations).where(models.event_invitations.c.event_id == event_id, models.event_invitations.c.user_id == user_id))
    await session.commit()
    await session.refresh(event)
    return event