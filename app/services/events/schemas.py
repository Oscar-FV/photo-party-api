from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional


class QuestCreate(BaseModel):
    name: str
    description: str
    event_id: UUID

class QuestResponse(BaseModel):
    id: UUID
    name: str
    description: str
    event_id: UUID

    class Config:
        from_attributes = True

class QuestLK(BaseModel):
    id: UUID
    name: str
    description: str
        
class EventResponse(BaseModel):
    id: UUID
    name: str
    starts_at: datetime
    ends_at: datetime
    is_active: Optional[bool]
    quests: Optional[List[QuestLK]] = []

    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    name: str
    description: str
    starts_at: datetime
    ends_at: datetime

class EventUpdate(BaseModel):
    name: Optional[str] = None
    descriptio: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    is_active: Optional[bool] = None
