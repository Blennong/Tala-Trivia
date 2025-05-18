from pydantic import BaseModel
from uuid import UUID

class TriviaQuestionCreate(BaseModel):
    trivia_id: UUID
    question_id: UUID

class TriviaQuestionResponse(BaseModel):
    id: UUID
    trivia_id: UUID
    question_id: UUID

    class Config:
        orm_mode = True
