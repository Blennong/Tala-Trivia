from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.schemas.question import QuestionResponse

class TriviaBase(BaseModel):
    title: str
    description: Optional[str] = None

class TriviaCreate(TriviaBase):
    pass

class TriviaResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    created_by_id: UUID
    created_at: datetime
    questions: list[QuestionResponse] = []

    class Config:
        orm_mode = True
