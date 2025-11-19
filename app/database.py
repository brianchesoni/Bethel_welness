from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get the database URL directly from Render environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine and session
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for debug logs
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Optional: safe table creation
def init_db():
    from app.models import *  # import all models
    Base.metadata.create_all(bind=engine)
