from sqlalchemy.orm import Session
from uuid import UUID
from app.models.models import TriviaQuestion, Question
from app.schemas.question import QuestionCreate, QuestionUpdate

def create_question(question_data: QuestionCreate, db: Session) -> Question:
    new_question = Question(
        text=question_data.text,
        category=question_data.category,
        difficulty=question_data.difficulty,
        correct_answer=question_data.correct_answer,
        options=question_data.options
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

def get_all_questions(db: Session) -> list[Question]:
    return db.query(Question).all()

def get_question_by_id(question_id: UUID, db: Session) -> Question | None:
    return db.query(Question).filter(Question.id == question_id).first()

def update_question_by_id(question_id: UUID, update_data: QuestionUpdate, db: Session) -> Question | None:
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return None

    for key, value in update_data.dict().items():
        setattr(question, key, value)

    db.commit()
    db.refresh(question)
    return question

def delete_question_by_id(question_id: UUID, db: Session) -> bool:
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return False

    db.delete(question)
    db.commit()
    return True

def get_questions_by_trivia_id(trivia_id: UUID, db: Session) -> list[Question]:
    trivia_questions = (
        db.query(Question)
        .join(TriviaQuestion, TriviaQuestion.question_id == Question.id)
        .filter(TriviaQuestion.trivia_id == trivia_id)
        .all()
    )
    return trivia_questions