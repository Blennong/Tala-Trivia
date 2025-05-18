from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.schemas.trivia import TriviaCreate, TriviaResponse
from app.database import get_db
from app.services.trivia_service import (
    create_trivia,     
    get_all_trivias, 
    get_trivia_by_id, 
    delete_trivia_by_id
)
from app.services.dependencies import get_current_user
from app.models.models import User

router = APIRouter(prefix="/trivias", tags=["Trivias"])

#Crear trivia
@router.post("/", response_model=TriviaResponse, status_code=status.HTTP_201_CREATED)
def create_trivia_endpoint(
    trivia_data: TriviaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_trivia(trivia_data, db, current_user)

# Listar todas las trivias
@router.get("/", response_model=List[TriviaResponse])
def list_trivias_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_trivias(db)


# Obtener trivia por ID
@router.get("/{trivia_id}", response_model=TriviaResponse)
def get_trivia_endpoint(
    trivia_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trivia = get_trivia_by_id(trivia_id, db)
    if not trivia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trivia no encontrada")
    return trivia


# Eliminar trivia por ID
@router.delete("/{trivia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trivia_endpoint(
    trivia_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_trivia_by_id(trivia_id, db)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trivia no encontrada")
    return