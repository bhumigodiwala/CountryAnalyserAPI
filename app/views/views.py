# views.py -> Consists of all API endpoints to generate different views
from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.security import OAuth2PasswordBearer
from controllers.controllers import authenticate_user, create_token, get_user_by_username, get_current_user, get_country_currencies_from_api, analyze_market
from models.models import SessionLocal, User
import requests

# Call the API app using FastAPI
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# API endpoint for GET request 
@app.get("/")
def read_root():
    return ("Welcome to Country Analyser API!")

# API endpoint for Token Veification
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

# API endpoint for Siging Up new users into database
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

# API endpoint for GET Response from the API link (To understand esponse json data obtained from the API link)
@app.get("/countries")
async def get_countries():
    response = requests.get("https://restcountries.com/v3.1/all")
    countries = response.json()
    return countries

# API endpoint for ML algorithm results
@app.get("/ml-analysis")
async def ml_analysis(current_user: dict = Depends(get_current_user)):
    # Fetch user activities and country currencies
    db = SessionLocal()
    users = db.query(User).all()
    user_activities = [user.website_activity for user in users]
    country_currencies = get_country_currencies_from_api()
    # Run ML analysis
    suggestion = analyze_market(user_activities, country_currencies)

    return {"message": "ML analysis result", "suggestion": suggestion}