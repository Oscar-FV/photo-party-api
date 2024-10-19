import logging
from celery import shared_task
from celery.result import AsyncResult
from sqlalchemy.orm import Session

from app.core.db import get_db
from .models import Event, Quest
from uuid import UUID
from datetime import datetime, timedelta, timezone

# CRUD para Event
def create_event(db: Session, event_data):
    new_event = Event(**event_data)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def get_event_by_id(db: Session, event_id: UUID):
    return db.query(Event).filter(Event.id == event_id).first()

def get_all_events(db: Session):
    return db.query(Event).all()

def get_events_starting_now(db: Session):
    current_time = datetime.now(timezone.utc)
    window_start = current_time - timedelta(seconds=30)
    window_end = current_time + timedelta(seconds=60)  
    events = db.query(Event).filter(
        Event.is_active == False,
        Event.starts_at >= window_start,
        Event.starts_at <= window_end
    ).all()
    
    return events

def update_event(db: Session, event_id: UUID, event_data: dict):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        return None
    for key, value in event_data.items():
        if value is not None:
            setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event

def delete_event(db: Session, event_id: UUID):
    event = db.query(Event).filter(Event.id == event_id).first()
    if event:
        db.delete(event)
        db.commit()
    return event

# CRUD para Quest
def create_quest(db: Session, quest_data):
    new_quest = Quest(**quest_data)
    db.add(new_quest)
    db.commit()
    db.refresh(new_quest)
    return new_quest

def get_quests_by_event(db: Session, event_id: UUID):
    return db.query(Quest).filter(Quest.event_id == event_id).all()

def delete_quest(db: Session, quest_id: UUID):
    quest = db.query(Quest).filter(Quest.id == quest_id).first()
    if quest:
        db.delete(quest)
        db.commit()
    return quest
