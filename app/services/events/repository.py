import logging
import random
from celery import shared_task
from celery.result import AsyncResult
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.services.events.schemas import QuestUser
from app.services.posts.models import Post
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

def get_event_start(db: Session, event_id: UUID):
    return db.query(Event).filter(Event.id == event_id).first().starts_at

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
    # Selección aleatoria de color e imagen
    colors = ["primary-500", "secondary-500", "accent-500", "card"]
    images = ["bat", "ghost", "hat", "pumpkin"]

    # Asignar valores aleatorios de color e imagen
    quest_data["color"] = random.choice(colors)
    quest_data["image"] = random.choice(images)

    # Crear el nuevo quest con los datos actualizados
    new_quest = Quest(**quest_data)
    db.add(new_quest)
    db.commit()
    db.refresh(new_quest)
    return new_quest

def get_quests_by_event(db: Session, event_id: UUID):
    return db.query(Quest).filter(Quest.event_id == event_id).all()

def get_quests_by_id(db: Session, quest_id: UUID):
    return db.query(Quest).filter(Quest.id== quest_id).first()

def get_all_quests_with_completion_status(db: Session, user_id: UUID, event_id: UUID):
    all_quests = db.query(
        Quest.id,
        Quest.name,
        Quest.description,
        Quest.color,
        Quest.image,
        func.count(Post.id).label("posts_count") 
    ).outerjoin(
        Post, (Post.quest_id == Quest.id) & (Post.user_id == user_id)  
    ).group_by(
        Quest.id
    ).filter(Quest.event_id == event_id).all()

    quests_with_status = [
        QuestUser(
            id=quest.id,
            name=quest.name,
            description=quest.description,
            is_completed=quest.posts_count > 0,
            color=quest.color,
            image=quest.image,
        )
        for quest in all_quests
    ]

    quests_with_status.sort(key=lambda x: x.is_completed)

    return quests_with_status


def delete_quest(db: Session, quest_id: UUID):
    quest = db.query(Quest).filter(Quest.id == quest_id).first()
    if quest:
        db.delete(quest)
        db.commit()
    return quest
