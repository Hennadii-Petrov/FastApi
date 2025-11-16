from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
from psycopg.rows import dict_row
from .config import settings

# For psycopg3, use postgresql+psycopg instead of postgresql
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

connection = None
cursor = None

try:
    connection = psycopg.connect(
        host="localhost",
        dbname="fastapi",
        user="postgres",
        password="0991",  # Correct password
        autocommit=True,
        row_factory=dict_row
    )
    cursor = connection.cursor()
    print("Database connection successful")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    print(f"Error type: {type(e).__name__}")
    print("App will continue without database connection...")