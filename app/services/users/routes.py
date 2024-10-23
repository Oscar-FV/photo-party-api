from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.services.users.models import Person
from .schemas import TokenRefreshRequest, TokenSchema, UserCreate, UserResponse
from .repository import authenticate_user, create_user
from app.core.db import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.post("/login", response_model=TokenSchema)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    event_id: str = Query(None)  # Parámetro opcional en la solicitud de login
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={"sub": user.email, "event_id": event_id}, 
        expires_delta=access_token_expires
    )

    # Generar un refresh token
    refresh_token = create_refresh_token()
    
    # Guardar el refresh token en la base de datos
    user.refresh_token = refresh_token
    db.add(user)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh-token", response_model=TokenSchema)
def refresh_access_token(request: TokenRefreshRequest, db: Session = Depends(get_db)):
    # Buscar el usuario en la base de datos por el refresh token
    user = db.query(Person).filter(Person.refresh_token == request.refresh_token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    # Generar un nuevo access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Devolver el nuevo access token, no es necesario devolver un nuevo refresh token
    return {
        "access_token": access_token,
        "refresh_token": user.refresh_token,  # En caso de que quieras devolver el mismo refresh token
        "token_type": "bearer"
    }
