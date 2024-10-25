from datetime import datetime
import logging
import os
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.core.security import get_current_user
from app.services.events.repository import get_events_starting_now
from app.services.users.models import Person
from app.services.users.schemas import CurrentUser
from .services.users.routes import router as user_router
from .services.events.routes import router as events_router
from .services.events.quests.routes import router as quests_router
from .services.posts.routes import router as posts_router

import app.init_db

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://bcea-187-245-73-217.ngrok-free.app" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

logging.basicConfig(level=logging.INFO)

@app.on_event("startup")
@repeat_every(seconds=60)  # Revisa cada 60 segundos
def activate_events_task():
    
    # Crear manualmente la sesión de la base de datos
    db: Session = SessionLocal()
    
    try:
        # Obtener eventos que deben empezar en este momento
        events = get_events_starting_now(db)
        
        for event in events:
            event.is_active = True
            db.commit()
    
    finally:
        db.close() 

@app.get("/me")
def read_users_me(current_user: CurrentUser = Depends(get_current_user)):
    return current_user


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(events_router, prefix="/events", tags=["events"])
app.include_router(quests_router, prefix="/quests", tags=["quests"])
app.include_router(posts_router, prefix="/posts", tags=["posts"])

