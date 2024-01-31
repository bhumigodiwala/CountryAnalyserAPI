from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.security import OAuth2PasswordBearer
from controllers.controllers import authenticate_user, create_token, verify_token, get_user_by_username, get_current_user
from models.models import SessionLocal, User
import requests

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@app.get("/")
def read_root():
    return ("Welcome to Country Analyser API!")

@app.post("/token")
async def login_for_access_token(username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_token({"sub": user["sub"]})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/signup")
async def signup(username: str = Form(...), password: str = Form(...), country: str = Form(...)):
    # Check if the username already exists
    existing_user = get_user_by_username(username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered",
        )

    # Checking if the country exists
    db_user = User(username=username, hashed_password=password, country=country)
    db = SessionLocal()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return {"message": "User created successfully"}

