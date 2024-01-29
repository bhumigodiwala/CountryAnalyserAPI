from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, Table
from databases import Database

# Configure database
DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()