from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.models import User, Trivia, Question, Attempt, Answer
from app.schemas.answer import AttemptCreate
from app.services.dependencies import get_current_user

router = APIRouter(prefix="/attempts", tags=["Attempts"])

# Crear intento y guardar respuestas
@router.post("/{trivia_id}", status_code=status.HTTP_201_CREATED)
def create_attempt_endpoint(
    trivia_id: UUID,
    attempt_data: AttemptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trivia = db.query(Trivia).filter(Trivia.id == trivia_id).first()
    if not trivia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trivia no encontrada")

    # Crear intento
    attempt = Attempt(user_id=current_user.id, trivia_id=trivia_id)
    db.add(attempt)
    db.flush()

    # Puntaje por dificultad
    difficulty_score = {
        "facil": 10,
        "medio": 20,
        "dificil": 30
    }

    score = 0

    for ans in attempt_data.answers:
        question = db.query(Question).filter(Question.id == ans.question_id).first()
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pregunta {ans.question_id} no encontrada")

        is_correct = ans.selected.strip().lower() == question.correct_answer.strip().lower()
        
        if is_correct:
            puntaje = difficulty_score.get(question.difficulty.lower(), 0)
            score += puntaje

        answer = Answer(
            attempt_id=attempt.id,
            question_id=ans.question_id,
            selected=ans.selected,
            is_correct=is_correct
        )
        db.add(answer)

    attempt.score = score
    db.commit()
    db.refresh(attempt)

    return {"attempt_id": attempt.id, "score": attempt.score}
