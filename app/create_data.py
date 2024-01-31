# create_data.py
from sqlalchemy.orm import Session
from faker import Faker
from models.models import SessionLocal, User, Base, engine  # Update this line with the correct path

fake = Faker()

def create_mock_user(db: Session):
    for _ in range(10):
        country = fake.country()
        username = fake.user_name()
        password = fake.password()
        db_user = User(username=username, hashed_password=password, country=country)
        db.add(db_user)
    db.commit()

if __name__ == "__main__":
    # Use SessionLocal to interact with the database
    db = SessionLocal()

    # Now create mock users
    create_mock_user(db)
