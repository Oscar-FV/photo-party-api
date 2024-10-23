from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID

class PostCreate(BaseModel):
    quest_id: UUID
    image_url: str
    caption: str = None
    

class PostRespone(PostCreate):
    id: UUID
    user_id: UUID
    created_at: datetime
    class Config:
        from_attributes = True
        
class PostLK(BaseModel):
    id: UUID
    image_url: str
    caption: str
    quest_name: str
    
class PostUserInfo(PostLK):
    user_name: str

class PostResponeWithPagination(BaseModel):
    posts: List[PostRespone] 
    has_more: bool

class PostLKWithPagination(BaseModel):
    posts: List[PostLK]  
    has_more: bool 
    
class PostUserInfoWithPagination(BaseModel):
    posts: List[PostUserInfo]  
    has_more: bool 