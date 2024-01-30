from sqlalchemy.orm import Session
from faker import Faker
from app.main import SessionLocal, User

fake = Faker()

def create_mock_user(db: Session):
    country = "USA"  
    for _ in range(10):
        username = fake.user_name()
        password = fake.password()
        db_user = User(username=username, hashed_password=password, country=country)
        db.add(db_user)
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    create_mock_user(db)
