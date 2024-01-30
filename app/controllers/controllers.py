from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from app.models.models import SessionLocal, User
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'P@ssW0rd'
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token, credentials_exception)
    return payload.get("sub")

def authenticate_user(username: str, password: str):
    db_user = get_user_by_username(username)
    if db_user and db_user.hashed_password == password:
        return {"sub": db_user.username}
    return None

def get_user_by_username(username: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception
