from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.db import get_db
from app.services.users.schemas import CurrentUser
from ..repository import create_quest, get_all_quests_with_completion_status, get_quests_by_event, delete_quest, get_quests_by_id
from ..schemas import QuestCreate, QuestResponse, QuestUser
from app.core.security import get_current_user


router = APIRouter()

# Routes for Quests

@router.post("", response_model=QuestResponse)
def create_quest_route(
    quest: QuestCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return create_quest(db, quest.dict())


@router.get("", response_model=List[QuestResponse])
def get_quests(
    db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)
):
    user = current_user["user"]
    event_id: UUID = current_user["event_id"]
    return get_quests_by_event(db, event_id)

@router.get("/quests-status", response_model=List[QuestUser])
def get_quests_status(
    db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)
):
    return get_all_quests_with_completion_status(db, current_user.user.id, current_user.event_id)

@router.get("/{quest_id}", response_model=QuestResponse)
def get_quests(
    quest_id: UUID, db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)
):
    return get_quests_by_id(db, quest_id)


@router.delete("/{quest_id}")
def delete_quest_route(
    quest_id: UUID,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    quest = delete_quest(db, quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    return {"detail": "Quest deleted"}
