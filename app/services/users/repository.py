from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from .models import Person, User
from .schemas import UserCreate

def create_user(db: Session, user: UserCreate):
    existing_person = db.query(Person).filter(Person.email == user.person.email).first()
    
    if existing_person:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario no está disponible. Prueba con una opción diferente.",
        )
    
    hashed_password = get_password_hash(user.person.password)
    person = Person(
        name=user.person.name,
        lastName=user.person.lastName,
        email=user.person.email,
        password=hashed_password
    )
    db.add(person)
    db.commit()
    db.refresh(person)
    
    user_obj = User(personId=person.id, role=user.role)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    
    return user_obj

def authenticate_user(db: Session, email: str, password: str):
    person = db.query(Person).filter(Person.email == email).first()
    if not person:
        return False
    if not verify_password(password, person.password):
        return False
    return person
