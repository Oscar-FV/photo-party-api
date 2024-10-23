import uuid
from sqlalchemy import UUID, Boolean, Column, DateTime, String, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.db import Base
from ..posts.models import Post


class Event(Base):
    __tablename__ = "events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    starts_at = Column(DateTime(timezone=True), default=func.now())
    ends_at = Column(DateTime(timezone=True), default=func.now())
    password = Column(String)
    is_active = Column(Boolean, nullable=True, default=False)
    task_id = Column(String, nullable=True)

    quests = relationship("Quest", back_populates="event")

class Quest(Base):
    __tablename__ = "quests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    name = Column(String)
    description = Column(String)
    
    event = relationship("Event", back_populates="quests")
    posts = relationship("Post", back_populates="quest")
