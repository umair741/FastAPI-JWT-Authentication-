from pydantic import BaseModel
from typing import Optional

class UserSignup(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"

