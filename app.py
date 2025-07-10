from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import engine, SessionLocal, get_db
from models import UserDetail, Base
from passlib.context import CryptContext
from jose import jwt
from typing import Optional

# Load environment variables
from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI(title="Signup API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database schema
Base.metadata.create_all(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # Set a secure key in .env
ALGORITHM = "HS256"

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    mobile: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    message: str

# Helper functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Signup API
@app.post("/signup", response_model=Token)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if email already exists
        db_user = db.query(UserDetail).filter(UserDetail.email == user.email, UserDetail.is_deleted == False).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash password and create user
        hashed_password = get_password_hash(user.password)
        db_user = UserDetail(
            email=user.email,
            password=hashed_password,
            name=user.name,
            mobile=user.mobile
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Create JWT token
        access_token = create_access_token(data={"sub": str(db_user.id)})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": db_user.id,
            "message": "User created successfully"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# Login API
@app.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        # Check if user exists
        db_user = db.query(UserDetail).filter(UserDetail.email == user.email, UserDetail.is_deleted == False).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verify password
        if not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=400, detail="Invalid password")

        # Create JWT token
        access_token = create_access_token(data={"sub": str(db_user.id)})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": db_user.id,
            "message": "Login successful"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8060))
    uvicorn.run(app, host="0.0.0.0", port=port)
