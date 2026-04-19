from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import UserProfile
from app.schemas.user_schema import UserCreate, UserResponse


router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
        Create a new user.
    """
    # 1. Check if the email already exists in the database
    db_user = db.query(UserProfile).filter(UserProfile.email == user_in.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    # 2. Convert Pydantic schema to SQLAlchemy model using model_dump()
    new_user = UserProfile(**user_in.model_dump())
    
    # 3. Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Retrieves the newly generated UUID from Postgres
    
    return new_user
