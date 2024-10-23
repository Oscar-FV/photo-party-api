from uuid import UUID
from sqlalchemy.orm import Session

from app.services.events.models import Quest
from app.services.posts.models import Post
from app.services.posts.schemas import PostCreate
from app.services.users.models import Person, User

def create_post(db: Session, post_data, user_id):
    new_post = Post(**post_data)
    new_post.user_id = user_id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_posts_by_user(db: Session, user_id: UUID, skip: int, limit: int):
    posts = db.query(
        Post.id,        
        Post.image_url,  
        Post.caption,    
        Quest.name.label("quest_name") 
    ).join(
        Quest, Post.quest_id == Quest.id 
    ).filter(Post.user_id == user_id).offset(skip).limit(limit + 1).all()
    
    has_more = len(posts) > limit
    posts = posts[:limit]
    
    return {"posts": posts, "has_more": has_more}

def get_posts_by_quest(db: Session, quest_id: UUID, skip: int, limit: int):
    posts = db.query(
        Post.id,                   
        Post.image_url,            
        Post.caption,              
        Quest.name.label("quest_name"),  
        Person.email.label("user_name")   
    ).join(
        Quest, Post.quest_id == Quest.id  
    ).join(
        User, Post.user_id == User.id  
    ).join(
        Person, User.personId == Person.id  
    ).filter(Post.quest_id == quest_id).offset(skip).limit(limit + 1).all()
    
    has_more = len(posts) > limit
    posts = posts[:limit]
    
    return {"posts": posts, "has_more": has_more}

def get_all_event_posts(db: Session, event_id: UUID, skip: int, limit: int):
    posts = db.query(
        Post.id,                   
        Post.image_url,            
        Post.caption,              
        Quest.name.label("quest_name"),  
        Person.email.label("user_name")   
    ).join(
        Quest, Post.quest_id == Quest.id  
    ).join(
        User, Post.user_id == User.id  
    ).join(
        Person, User.personId == Person.id  
    ).filter(Quest.event_id == event_id).offset(skip).limit(limit + 1).all()
    
    has_more = len(posts) > limit
    posts = posts[:limit]
    
    return {"posts": posts, "has_more": has_more}