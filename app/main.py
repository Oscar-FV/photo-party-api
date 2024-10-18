from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.security import get_current_user, is_admin
from app.services.users.models import Person
from .services.users.routes import router as user_router
from .services.events.routes import router as events_router
import app.init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto a los dominios que necesites permitir, o usa "*" para todos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

@app.get("/me")
def read_users_me(current_user: Person = Depends(is_admin)):
    return current_user


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(events_router, prefix="/events", tags=["events"])

