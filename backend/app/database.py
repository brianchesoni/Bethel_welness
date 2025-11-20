from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get the database URL from Render environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import models
from app.models import Product, Preorder, Order

# Initialize tables
def init_db():
    Base.metadata.create_all(bind=engine)
