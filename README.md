# FastAPI Authentication Example

This is a simple **FastAPI** project that demonstrates user authentication and role-based access control using **JWT tokens**.

## Features
- User signup with password hashing (`bcrypt`)
- User login with JWT token generation
- Protected routes (accessible to logged-in users)
- Admin-only routes (role-based access control)
- In-memory database (`fake_db`) for learning purposes

## Tech Stack
- FastAPI
- Uvicorn
- Passlib (bcrypt)
- python-jose

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/fastapi-auth-example.git
cd fastapi-auth-example

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac
source venv/bin/activate
# On Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

unning the App
uvicorn main:app --reload


Now open in browser:
👉 http://127.0.0.1:8000/docs

API Endpoints

POST /signup → Create a new user

POST /login → Authenticate user and get JWT token

GET /protected → Accessible only to authenticated users

GET /admin-only → Accessible only to admin role

Notes

Uses in-memory fake_db.

Not for production use (replace with real database + env variables for secret key).