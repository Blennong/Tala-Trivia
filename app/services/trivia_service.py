from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from fastapi import HTTPException, status
from app.models.models import Trivia, User, TriviaQuestion, Question
from app.schemas.trivia import TriviaCreate


def create_trivia(trivia_data: TriviaCreate, db: Session, user: User) -> Trivia:
    # VAlida título obligatorio
    if not trivia_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El título de la trivia no puede estar vacío."
        )

    # Valida que las preguntas existan y eliminar duplicados
    question_ids = list(set(trivia_data.question_ids))
    if question_ids:
        existing_questions = db.query(Question.id).filter(Question.id.in_(question_ids)).all()
        found_ids = {q.id for q in existing_questions}
        missing_ids = set(question_ids) - found_ids
        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Preguntas no encontradas: {', '.join(str(i) for i in missing_ids)}"
            )

    # Valida usuarios asignados
    assigned_users = []
    if trivia_data.assigned_user_ids:
        assigned_users = db.query(User).filter(User.id.in_(trivia_data.assigned_user_ids)).all()
        found_user_ids = {u.id for u in assigned_users}
        missing_users = set(trivia_data.assigned_user_ids) - found_user_ids
        if missing_users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuarios no encontrados: {', '.join(str(u) for u in missing_users)}"
            )

    # Crear trivia
    try:
        new_trivia = Trivia(
            title=trivia_data.title.strip(),
            description=trivia_data.description,
            created_by_id=user.id
        )
        db.add(new_trivia)
        db.flush()

        # Asociar preguntas
        for question_id in question_ids:
            trivia_question = TriviaQuestion(
                trivia_id=new_trivia.id,
                question_id=question_id
            )
            db.add(trivia_question)

        # Asociar usuarios
        if hasattr(new_trivia, "assigned_users") and assigned_users:
            new_trivia.assigned_users = assigned_users

        db.commit()
        db.refresh(new_trivia)
        return new_trivia

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear la trivia. Verifica que los datos sean válidos."
        )

#Trae todas las trivias
def get_all_trivias(db: Session) -> list[Trivia]:
    trivias = db.query(Trivia).all()
    return trivias

#Trae una trivia por su UUID
def get_trivia_by_id(trivia_id: UUID, db: Session) -> Trivia:
    trivia = db.query(Trivia).filter(Trivia.id == trivia_id).first()
    if not trivia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una trivia con ID: {trivia_id}"
        )
    return trivia

#Borra una trivia por su UUID
def delete_trivia_by_id(trivia_id: UUID, db: Session) -> bool:
    trivia = db.query(Trivia).filter(Trivia.id == trivia_id).first()
    if not trivia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró una trivia con ID: {trivia_id}"
        )
    db.delete(trivia)
    db.commit()
    return True
