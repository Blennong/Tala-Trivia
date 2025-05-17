from datetime import datetime
from pydantic import BaseModel

class AttemptCreate(BaseModel):
  trivia_id: int

class AttemptOut(BaseModel):
  id: int
  user_id: int
  trivia_id: int
  score: float
  submitted_at: datetime

  class Config:
    orm_mode = True
