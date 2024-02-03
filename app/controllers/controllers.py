#controllers.py -> Defines all the methods to perform variety of tasks, Authentication using HS256 algorithm
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from models.models import SessionLocal, User
from fastapi.security import OAuth2PasswordBearer

from typing import List
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import requests
import pandas as pd

# Define Authentication Scheme and also a secret key and algorithm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'P@ssW0rd' #secret key can be stored in a separate config file to maintain privacy
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme)):
    '''
    Authenticates and gets the current user from the database
    Verifies user access token
    
    '''

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token, credentials_exception)
    return payload.get("sub")

def get_user_by_username(username: str):
    '''
    username: input username string

    Gets user information with help of username
    '''
    
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user

def authenticate_user(username: str, password: str):
    '''
    username: input username
    password: username's password to login

    Authenticates users using combination of username and password
    
    '''
    
    db_user = get_user_by_username(username)
    if db_user and db_user.hashed_password == password:
        return {"sub": db_user.username}
    return None

def create_token(data: dict):
    '''
    data: input data from the database

    Creates tokens for a pair of username, password, country data from the database
    
    '''
    
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, credentials_exception):
    '''
    token: access token generated for a specific username and password

    Verifies the token generated for a pair of username and password
    
    '''
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception

def get_currency_from_country(country_data):
    '''
    country_data: response json data from the rest api link

    Extract and returns the currency information from the country data response json
    This country data is ontained from the rest api link: https://restcountries.com/v3.1/all
    
    '''
    # Extract the currency information from the Rest Countries API response
    curr = list(country_data.get("currencies", {}).keys())
    currencies = list(set(curr))
    # print(currencies)

    if currencies and isinstance(currencies, list) and currencies[0]:
        return currencies[0]

    return "N/A"

def get_country_currencies_from_api():
    '''
    Fetches all the countries data from the rest api link
    Retrieves the currency information from the above countries data

    '''
    
    # Fetch the countries data from the API
    response = requests.get("https://restcountries.com/v3.1/all")
    # Store countries data response in json format
    countries_data = response.json()
    # Extract country names and currencies
    countries = [country['name']['common'] for country in countries_data]
    currencies = [get_currency_from_country(country) for country in countries_data]

    # Return a list of tuples containing country and its currency
    return list(zip(countries, currencies))

def user_cat_to_num(user_activity):
    '''
    user_activity: user_activity(High, Medium, Low) from the database

    Return the conversion from user activity categorical data to numerical data

    '''
    if user_activity == 'High': 
        return 2
    elif user_activity == 'Medium':
        return 1
    else:
        return 0

def analyze_market(user_activities: List[str], country_currencies: List[tuple]):
    '''
    user_activities: user_activity from input database
    country_currencies: Pair of country names and currencies obtained from 'get_country_currencies_from_api' method

    Train and test a ML algorithm for market analysis
    Returns suggestion for market expansion

    '''
    
    # Create a dataset for the ML algorithm
    dataset = []
    for user_activity, (country, currency) in zip(user_activities, country_currencies):
        dataset.append({'user_activity': user_activity, 'country': country, 'currency': currency})

    # Convert dataset to DataFrame
    df = pd.DataFrame(dataset)

    # Encode categorical features
    label_encoder = LabelEncoder()
    df['country_code'] = label_encoder.fit_transform(df['country'])
    df['currency_code'] = label_encoder.fit_transform(df['currency'])
    df['user_act_code'] = label_encoder.fit_transform(df['user_activity'])

    df['y'] = df['user_activity'].apply(user_cat_to_num)

    # Split dataset into features (X) and target (y)
    X = df[['country_code','currency_code','user_act_code']]
    y = df['y']

    print(df)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=40)

    # Train a simple RandomForestClassifier
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, predictions)

    # Based on the accuracy, provide a suggestion
    if accuracy >= 0.8:
        suggestion = "High user activity detected. Consider Expanding here!"
    elif accuracy >= 0.5 and accuracy < 0.8:
        suggestion = "Medium user activity detected. Consider expanding in next few years!"
    else:
        suggestion = "Low user activity. Do not expand here!"

    return suggestion
