from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class TriviaBase(BaseModel):
  title: str
  description: Optional[str] = None

class TriviaCreate(TriviaBase):
  question_ids: List[int]

class TriviaOut(TriviaBase):
  id: int
  created_by_id: int
  created_at: datetime

  class Config:
    orm_mode = True
