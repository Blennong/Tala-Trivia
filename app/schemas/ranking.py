from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class RankingResponse(BaseModel):
    user_id: UUID
    username: str
    score: int
    submitted_at: datetime

    class Config:
        orm_mode = True
