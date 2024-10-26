from datetime import datetime, timedelta
import secrets
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import UUID
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.core.db import get_db
from app.services.users.models import Person, User
from app.services.users.schemas import CurrentUser, TokenData, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    
    # Incluir event_id en el JWT si está presente en `data`
    if "event_id" in data:
        to_encode.update({"event_id": data["event_id"]})
    
    print(to_encode)

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        event_id: Optional[UUID] = payload.get("event_id")
        
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    db_user = db.query(User).join(Person).filter(Person.email == token_data.email).first()
    if db_user is None:
        raise credentials_exception
    
    user_response = UserResponse.model_validate(db_user)
    
    current_user = CurrentUser(
        user=user_response,
        event_id=event_id
    )
    return current_user


def create_refresh_token():
    return secrets.token_hex(32)