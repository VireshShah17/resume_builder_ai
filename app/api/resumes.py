from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import UserProfile
from app.models.resume import ResumeProject
from app.schemas.resume_schema import ResumeProjectCreate, ResumeProjectResponse

router = APIRouter()


@router.post("/", response_model=ResumeProjectResponse, status_code=status.HTTP_201_CREATED)
def create_resume_project(resume_in: ResumeProjectCreate, db: Session = Depends(get_db)):
    """
        Create a new resume project for a specific user.
    """
    # 1. Verify the user actually exists in the database first
    user = db.query(UserProfile).filter(UserProfile.user_id == resume_in.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found. Cannot create resume for a non-existent user."
        )
    
    # 2. Create the resume project
    new_resume = ResumeProject(**resume_in.model_dump())
    
    # 3. Save to database
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume) 
    
    return new_resume