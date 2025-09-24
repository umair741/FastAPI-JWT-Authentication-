from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .auth import decode_access_token
from .db import fake_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")
    user = fake_db.get(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def get_current_admin(token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user
