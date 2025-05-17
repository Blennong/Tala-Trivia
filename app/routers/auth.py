from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse
from app.models import models
from app.database import get_db
from app.services.auth_service import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.email == credentials.email).first()

  if not user or not verify_password(credentials.password, user.password_hash):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid email or password"
    )

  token = create_access_token({"sub": str(user.id)})
  return {"access_token": token}
