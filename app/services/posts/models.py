from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime, func, UUID
from sqlalchemy.orm import relationship
from app.core.db import Base
import uuid


class Post(Base):
    __tablename__ = 'posts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    quest_id = Column(UUID(as_uuid=True), ForeignKey("quests.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    image_url = Column(String, nullable=False)
    caption = Column(String, nullable=True) 
    is_active = Column(Boolean, default=True)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    quest = relationship("Quest", back_populates="posts")
    user = relationship("User", back_populates="posts")