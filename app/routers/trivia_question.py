from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.trivia_question import TriviaQuestionCreate, TriviaQuestionResponse
from app.services.trivia_question_service import add_question_to_trivia, remove_question_from_trivia
from app.services.dependencies import get_current_user
from app.models.models import User

router = APIRouter(prefix="/trivia-questions", tags=["Trivia Questions"])

# Asociar pregunta a trivia
@router.post("/", response_model=TriviaQuestionResponse, status_code=status.HTTP_201_CREATED)
def add_question(
    data: TriviaQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return add_question_to_trivia(data, db)

# Eliminar asociación pregunta-trivia
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def remove_question(
    data: TriviaQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = remove_question_from_trivia(data.trivia_id, data.question_id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asociación no encontrada")
