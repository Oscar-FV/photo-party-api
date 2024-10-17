import uuid
from sqlalchemy import UUID, Boolean, Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base


class Event(Base):
    __tablename__ = "events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String)
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)
    password = Column(String)
    isActive = Column(Boolean, default=False)

    quests = relationship("Quest", back_populates="event")

class Quest(Base):
    __tablename__ = "quests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    name = Column(String)
    description = Column(String)
    
    event = relationship("Event", back_populates="quests")
