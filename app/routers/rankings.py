from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.models import Trivia, Attempt, User
from app.services.dependencies import get_current_user
from app.schemas.ranking import RankingResponse

router = APIRouter(prefix="/rankings", tags=["Rankings"])

# Obtener el ranking de una trivia
@router.get("/{trivia_id}", response_model=List[RankingResponse])
def get_ranking_endpoint(
    #TO-DO: AGREGAR PAGINACION
    trivia_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trivia = db.query(Trivia).filter(Trivia.id == trivia_id).first()
    if not trivia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trivia no encontrada")

    attempts = (
        db.query(Attempt)
        .filter(Attempt.trivia_id == trivia_id)
        .order_by(Attempt.score.desc(), Attempt.submitted_at.asc())
        .limit(10)
        .all()
    )

    rankings = [
        RankingResponse(
            user_id=attempt.user_id,
            username=attempt.user.username,
            score=attempt.score,
            submitted_at=attempt.submitted_at
        )
        for attempt in attempts
    ]

    return rankings
