from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import UserSignup
from .auth import hash_password, verify_password, create_access_token
from .deps import get_current_user, get_current_admin
from .db import fake_db

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/signup")
def signup(user: UserSignup):
    if user.username in fake_db:
        raise HTTPException(status_code=400, detail="This username already exists")

    hashed_pass = hash_password(user.password)

    fake_db[user.username] = {
        "username": user.username,
        "hashed_password": hashed_pass,
        "role": user.role,
    }

    return {"msg": f"User {user.username} created successfully", "role": user.role}

@app.post("/login")
def login(user: UserSignup):
    if user.username not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")

    db_user = fake_db[user.username]

    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"sub": db_user["username"], "role": db_user["role"]})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "msg": f"Hello {current_user['username']}! You have access to this protected route.",
        "role": current_user["role"],
    }

@app.get("/admin-only")
def admin_route(current_user: dict = Depends(get_current_admin)):
    return {"msg": f"Hello Admin {current_user['username']}! You can access admin-only routes."}
