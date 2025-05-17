from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import user
from app.models import models
from app.database import get_db
from app.services import auth_service

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
def get_users(db: Session = Depends(get_db)):
  return db.query(models.User).all()


@router.get("/{user_id}", response_model=user.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == user_id).first()
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  return user
