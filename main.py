from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from typing import List
import secrets
import pandas as pd  

app = FastAPI()

# Configure SQLAlchemy
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    country = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# JWT
SECRET_KEY = 'P@ssW0rd'
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# Dependency to get the current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token, credentials_exception)
    return payload.get("sub")

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception

def get_user_by_username(username: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user

# Dependency to authenticate user
def authenticate_user(username: str, password: str):
    # Placeholder logic, replace with your actual user authentication logic
    # For example, check against a database of users
    db_user = get_user_by_username(username)
    if db_user and db_user.hashed_password == password:
        return {"sub": db_user.username}  # Returning the username in the JWT payload

    return None

# API Endpoints

@app.get("/")
def read_root():
    res = "Welcome to Country Analyser API"
    return res