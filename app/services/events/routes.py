from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime
import asyncio

from app.core.db import get_db
from .repository import (
    create_event, get_event_by_id, get_all_events, update_event,
    delete_event, create_quest, get_quests_by_event, delete_quest
)
from .schemas import EventCreate, EventResponse, EventUpdate, QuestCreate, QuestResponse
from app.core.security import get_current_user, is_admin
from app.services.users.models import Person  

router = APIRouter()

connected_clients = []

async def notify_event_active(event_id: UUID):
    for client in connected_clients:
        await client.send_text(f"Event {event_id} is now active!")
        
@router.websocket("/ws/{event_id}")
async def event_websocket(websocket: WebSocket, event_id: UUID, db: Session = Depends(get_db)):
    await websocket.accept()
    connected_clients.append(websocket)
    
    try:
        while True:
            await asyncio.sleep(30)  # Revisar el estado del evento cada 5 segundos
            event = get_event_by_id(db, event_id)
            
            if event and event.is_active:
                await notify_event_active(event_id)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        await websocket.close()

# Routes for Event
@router.post("/", response_model=EventResponse)
def create_event_route(event: EventCreate, db: Session = Depends(get_db), current_user: Person = Depends(is_admin)):
    return create_event(db, event.dict())

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: UUID, db: Session = Depends(get_db), current_user: Person = Depends(is_admin)):
    event = get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.get("/", response_model=List[EventResponse])
def get_all_events_route(db: Session = Depends(get_db), current_user: Person = Depends(get_current_user)):
    return get_all_events(db)

@router.put("/{event_id}/status")
def update_event_route(event_id: UUID, event_data: EventUpdate, db: Session = Depends(get_db), current_user: Person = Depends(is_admin)):
    updated_event = update_event(db, event_id, event_data.dict(exclude_unset=True))
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated_event

@router.delete("/{event_id}")
def delete_event_route(event_id: UUID, db: Session = Depends(get_db), current_user: Person = Depends(is_admin)):
    event = delete_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"detail": "Event deleted"}


# Routes for Quests

@router.post("/quests", response_model=QuestResponse)
def create_quest_route(quest: QuestCreate, db: Session = Depends(get_db), current_user: Person = Depends(is_admin)):
    return create_quest(db, quest.dict())

@router.get("/{event_id}/quests", response_model=List[QuestResponse])
def get_quests(event_id: UUID, db: Session = Depends(get_db), current_user: Person = Depends(get_current_user)):
    return get_quests_by_event(db, event_id)

@router.delete("/quests/{quest_id}")
def delete_quest_route(quest_id: UUID, db: Session = Depends(get_db), current_user: Person = Depends(is_admin)):
    quest = delete_quest(db, quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    return {"detail": "Quest deleted"}
