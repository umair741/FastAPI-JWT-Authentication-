from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional


SECRET_KEY = "your_random_secret_key_here"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake_db = {}

class UserSignup(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"  

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


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

# ----------------------
# Routes
# ----------------------
@app.post("/signup")
def signup(user: UserSignup):
    if user.username in fake_db:
        raise HTTPException(status_code=400, detail="This username already exists")

    hashed_pass = hash_password(user.password)

    fake_db[user.username] = {
        "username": user.username,
        "hashed_password": hashed_pass,
        "role": user.role
    }

    return {"msg": f"User {user.username} created successfully", "role": user.role}

@app.post("/login")
def login(user: UserSignup):
    # 1. Check user exists
    if user.username not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")

    db_user = fake_db[user.username]

    # 2. Verify password
    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    # 3. Create JWT token
    token = create_access_token({"sub": db_user["username"], "role": db_user["role"]})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "msg": f"Hello {current_user['username']}! You have access to this protected route.", 
        "role": current_user["role"]
    }

@app.get("/admin-only")
def admin_route(current_user: dict = Depends(get_current_admin)):
    return {"msg": f"Hello Admin {current_user['username']}! You can access admin-only routes."}
