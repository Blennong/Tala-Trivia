from uuid import UUID
from pydantic import BaseModel
from typing import List

class AnswerCreate(BaseModel):
    question_id: UUID
    selected: str

class AttemptCreate(BaseModel):
    answers: List[AnswerCreate]