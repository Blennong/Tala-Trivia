from pydantic import BaseModel

class AnswerCreate(BaseModel):
  question_id: int
  selected: str

class AnswerOut(BaseModel):
  id: int
  attempt_id: int
  question_id: int
  selected: str
  is_correct: bool

  class Config:
    orm_mode = True
