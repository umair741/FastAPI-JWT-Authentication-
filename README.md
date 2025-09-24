🚀 FastAPI JWT Authentication Example
A simple FastAPI application demonstrating JWT authentication and role-based access control using Python. Built with FastAPI, Passlib, Python-Jose, and Dotenv, it uses an in-memory fake DB for demonstration purposes.
✨ Features

User signup with secure password hashing (bcrypt)
User login with JWT token generation
Protected routes accessible only to authenticated users
Admin-only routes for role-based access control
Secure secrets management using .env

📦 Installation

Clone the repository:
git clone https://github.com/your-username/fastapi-auth-app.git
cd fastapi-auth-app


Create a virtual environment (recommended):
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows


Install dependencies:
pip install -r requirements.txt



⚙️ Environment Variables
Create a .env file in the project root with the following content:
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Note: Never commit your .env file to version control (already ignored via .gitignore).
▶️ Running the App
Start the FastAPI server using Uvicorn:
uvicorn app.main:app --reload

The server will run at:
http://127.0.0.1:8000

Access interactive API documentation:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

🔑 API Endpoints

Signup

Endpoint: POST /signup
Request Body:{
  "username": "john",
  "password": "mypassword",
  "role": "user"
}




Login

Endpoint: POST /login
Request Body:{
  "username": "john",
  "password": "mypassword"
}


Response: Returns a JWT token


Protected Route

Endpoint: GET /protected
Requires: Authorization: Bearer <token>


Admin-Only Route

Endpoint: GET /admin-only
Requires: Authorization: Bearer <token> with admin role



📂 Project Structure
fastapi-auth-app/
├── app/
│   ├── main.py       # FastAPI app and routes
│   ├── models.py     # Pydantic models
│   ├── auth.py       # Authentication utilities (hashing, JWT)
│   ├── deps.py       # Dependencies (current_user, current_admin)
│   └── db.py         # In-memory fake database
├── .env              # Environment variables (ignored)
├── requirements.txt  # Project dependencies
├── .gitignore        # Git ignore file
└── README.md         # Project documentation

⚠️ Disclaimer
This project uses an in-memory database (fake_db), which resets on server restart. For production, replace it with a persistent database (e.g., Postgres, MongoDB) and manage secrets using a secure vault.
🛠️ Tech Stack

FastAPI: Web framework
Uvicorn: ASGI server
Passlib: Password hashing
Python-Jose: JWT handling
Dotenv: Environment variable management
