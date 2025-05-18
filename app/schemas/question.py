from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import List

class QuestionBase(BaseModel):
    text: str
    category: str
    difficulty: str
    correct_answer: str
    options: List[str]

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
