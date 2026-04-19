# Import required libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create the SQLAlchemy engine
engine= create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base() # Create a base class for our models to inherit from

# Dependency to use in our API routes
def get_db():
    db = SessionLocal() # Create a new database session
    try:
        yield db # Yield the database session to be used in the API route
    finally:
        db.close() # Close the database session after the API route is done
