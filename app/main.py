from fastapi import Depends, FastAPI

from app.core.security import get_current_user, is_admin
from app.services.users.models import Person
from .services.users.routes import router as user_router
import app.init_db

app = FastAPI()

@app.get("/me")
def read_users_me(current_user: Person = Depends(is_admin)):
    return current_user


app.include_router(user_router, prefix="/users", tags=["users"])

