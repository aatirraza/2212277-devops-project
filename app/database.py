import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Fetch DB connection credentials from environment variables
DB_USER = os.getenv("DB_USER", "devops")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret123")
DB_HOST = os.getenv("DB_HOST", "db")  # 'db' matches our Docker Compose service name
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "appdb")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Resilient connection retry loop matching Class 5 guidelines
engine = None
for attempt in range(5):
    try:
        engine = create_engine(DATABASE_URL)
        # Force a quick connectivity check test
        with engine.connect() as conn:
            break
    except OperationalError:
        print(f"Database connection attempt {attempt + 1}/5 failed. Retrying in 2 seconds...")
        time.sleep(2)

if not engine:
    raise RuntimeError("Could not establish connection to the database after 5 attempts.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency provider function to yield database sessions to api endpoints safely
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
