import uuid
from sqlalchemy import UUID, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.db import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    guest = "guest"

class Person(Base):
    __tablename__ = "persons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String, index=True)
    lastName = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    refresh_token = Column(String, nullable=True)

    # Relación con la tabla User
    user = relationship("User", back_populates="person", uselist=False)

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    personId = Column(UUID(as_uuid=True), ForeignKey("persons.id"))
    role = Column(Enum(RoleEnum), default="guest")
    
    # Relación con la tabla Person
    person = relationship("Person", back_populates="user")
