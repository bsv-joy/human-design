from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables (ensure .env.local is loaded)
load_dotenv(os.path.join(os.path.dirname(__file__), '.env.local'))

# Replace with your actual PostgreSQL connection string
# DATABASE_URL is read from the environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL is None:
    raise Exception("DATABASE_URL environment variable is not set. Please create a .env.local file in the backend directory.")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
