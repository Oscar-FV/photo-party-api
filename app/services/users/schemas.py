from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str

class TokenData(BaseModel):
    email: str
    
class TokenRefreshRequest(BaseModel):
    refresh_token: str

class Login(BaseModel):
    email: str
    password: str

class PersonCreate(BaseModel):
    name: str
    lastName: str
    email: str
    password: str

class UserCreate(BaseModel):
    role: Optional[str] = "guest"
    person: PersonCreate

class UserResponse(BaseModel):
    id: UUID
    role: str
    person: PersonCreate

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
