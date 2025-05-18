from sqlalchemy.orm import Session
from uuid import UUID
from app.models.models import TriviaQuestion
from app.schemas.trivia_question import TriviaQuestionCreate

#TO-DO: Agregar validaciones
def add_question_to_trivia(data: TriviaQuestionCreate, db: Session) -> TriviaQuestion:
    trivia_question = TriviaQuestion(
        trivia_id=data.trivia_id,
        question_id=data.question_id
    )
    db.add(trivia_question)
    db.commit()
    db.refresh(trivia_question)
    return trivia_question

def remove_question_from_trivia(trivia_id: UUID, question_id: UUID, db: Session) -> bool:
    trivia_question = db.query(TriviaQuestion).filter_by(
        trivia_id=trivia_id,
        question_id=question_id
    ).first()
    if not trivia_question:
        return False
    db.delete(trivia_question)
    db.commit()
    return True
