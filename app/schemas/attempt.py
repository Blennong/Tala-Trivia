from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class AttemptCreate(BaseModel):
    trivia_id: int

class AttemptOut(BaseModel):
    id: UUID
    user_id: int
    trivia_id: int
    score: float
    submitted_at: datetime

    class Config:
        orm_mode = True
