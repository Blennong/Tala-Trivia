from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas import user
from app.models import models
from app.database import get_db
from app.services import auth_service
from app.services.dependencies import get_current_user
from app.models.models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=user.UserResponse)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Correo ya existe")

    hashed_password = auth_service.hash_password(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=list[user.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  
):
    return db.query(models.User).all()


@router.get("/{user_id}", response_model=user.UserResponse)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user