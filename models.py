# from pydantic import BaseModel
# from typing import Optional

# class UserSignup(BaseModel):
#     username: str
#     password: str
#     role: Optional[str] = "user"
import secrets
print(secrets.token_hex(32))
