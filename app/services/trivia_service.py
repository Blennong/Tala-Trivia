from sqlalchemy.orm import Session
from uuid import UUID
from app.models.models import Trivia, User, TriviaQuestion
from app.schemas.trivia import TriviaCreate

def create_trivia(trivia_data: TriviaCreate, db: Session, user: User) -> Trivia:
    # Crear la trivia base
    new_trivia = Trivia(
        title=trivia_data.title,
        description=trivia_data.description,
        created_by_id=user.id
    )
    db.add(new_trivia)
    db.flush()

    # Asociar preguntas
    for question_id in trivia_data.question_ids:
        trivia_question = TriviaQuestion(trivia_id=new_trivia.id, question_id=question_id)
        db.add(trivia_question)

    # Asociar usuarios asignados
    if hasattr(new_trivia, "assigned_users") and trivia_data.assigned_user_ids:
        users = db.query(User).filter(User.id.in_(trivia_data.assigned_user_ids)).all()
        new_trivia.assigned_users = users

    db.commit()
    db.refresh(new_trivia)
    return new_trivia


def get_all_trivias(db: Session) -> list[Trivia]:
    trivias = db.query(Trivia).all()
    return trivias


def get_trivia_by_id(trivia_id: UUID, db: Session) -> Trivia | None:
    trivia = db.query(Trivia).filter(Trivia.id == trivia_id).first()
    return trivia


def delete_trivia_by_id(trivia_id: UUID, db: Session) -> bool:
    trivia = db.query(Trivia).filter(Trivia.id == trivia_id).first()
    if not trivia:
        return False
    db.delete(trivia)
    db.commit()
    return True
