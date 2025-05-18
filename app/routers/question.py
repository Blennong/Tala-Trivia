from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.question import QuestionCreate, QuestionResponse, QuestionUpdate
from app.database import get_db
from app.services.question_service import (
    create_question,
    get_all_questions,
    get_question_by_id,
    update_question_by_id,
    delete_question_by_id,
    get_questions_by_trivia_id
)
from app.services.dependencies import get_current_user
from app.models.models import User

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.get("/trivia/{trivia_id}", response_model=List[QuestionResponse])
def list_questions_by_trivia(
    trivia_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    questions = get_questions_by_trivia_id(trivia_id, db)
    if not questions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron preguntas para esta trivia.")
    return questions

# Crear pregunta
@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question_endpoint(
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_question(question_data, db)

# Listar todas las preguntas
@router.get("/", response_model=List[QuestionResponse])
def list_questions_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_questions(db)

# Obtener pregunta por ID
@router.get("/{question_id}", response_model=QuestionResponse)
def get_question_endpoint(
    question_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    question = get_question_by_id(question_id, db)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregunta no encontrada")
    return question

# Actualizar pregunta por ID
@router.put("/{question_id}", response_model=QuestionResponse)
def update_question_endpoint(
    question_id: UUID,
    update_data: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_question = update_question_by_id(question_id, update_data, db)
    if not updated_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregunta no encontrada")
    return updated_question

# Eliminar pregunta por ID
@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question_endpoint(
    question_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_question_by_id(question_id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregunta no encontrada")
    return
