from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime
import asyncio

from app.core.db import get_db
from app.services.users.schemas import CurrentUser
from .repository import (
    create_event, get_event_by_id, get_all_events, get_event_start, update_event,
    delete_event
)
from .schemas import EventCreate, EventResponse, EventUpdate, QuestCreate, QuestResponse
from app.core.security import get_current_user 

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
@router.post("", response_model=EventResponse)
def create_event_route(event: EventCreate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    return create_event(db, event.dict())

@router.get("", response_model=List[EventResponse])
def get_all_events_route(db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    return get_all_events(db)

@router.get("/event-info", response_model=EventResponse)
def get_event(db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    
    event = get_event_by_id(db, current_user.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.get("/start-time", response_model=datetime)
def get_event_start_time( db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    print(current_user.event_id)
    event = get_event_start(db, current_user.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{event_id}")
def update_event_route(event_id: UUID, event_data: EventUpdate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    updated_event = update_event(db, event_id, event_data.dict(exclude_unset=True))
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated_event

@router.delete("/{event_id}")
def delete_event_route(event_id: UUID, db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    event = delete_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"detail": "Event deleted"}



