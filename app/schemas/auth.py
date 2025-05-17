from uuid import UUID
from pydantic import BaseModel

# class Token(BaseModel):
#   access_token: str
#   token_type: str = "bearer"

# class TokenData(BaseModel):
#   user_id: UUID

class LoginRequest(BaseModel):
  email: str
  password: str

class TokenResponse(BaseModel):
  access_token: str
  token_type: str = "bearer"