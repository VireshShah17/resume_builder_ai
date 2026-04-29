from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import UserProfile
from app.models.resume import ResumeProject, ResumeSection, SectionType, ExperienceDuty, GenerativeOption
from app.schemas.resume_schema import ResumeProjectCreate, ResumeProjectResponse, AIBulletRequest, AIBulletResponse
from app.services.llm_service import llm_service
import uuid

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


@router.post("/generate-bullets", response_model = AIBulletResponse, status_code = status.HTTP_200_OK)
async def generate_and_save_bullets(request: AIBulletRequest, db: Session = Depends(get_db)):
    """
        Takes raw user input, asks Gemini to generate 3 professional bullets, 
        and saves them to the database.
    """
    # 1. Verify the Resume Project exists
    resume = db.query(ResumeProject).filter(ResumeProject.resume_id == request.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume project not found.")

    # 2. Check if an "Experience" section exists for this resume; if not, create it
    section = db.query(ResumeSection).filter(
        ResumeSection.resume_id == request.resume_id,
        ResumeSection.section_type == SectionType.EXPERIENCE
    ).first()
    
    if not section:
        section = ResumeSection(resume_id=request.resume_id, section_type=SectionType.EXPERIENCE)
        db.add(section)
        db.commit()
        db.refresh(section)

    # 3. Create the "Duty Atom" to hold the raw input
    new_duty = ExperienceDuty(section_id=section.section_id, raw_input=request.raw_input)
    db.add(new_duty)
    db.commit()
    db.refresh(new_duty)

    # 4. CALL THE AI BRAIN
    generated_texts = await llm_service.generate_experience_bullets(
        target_role=request.target_role, 
        raw_input=request.raw_input
    )

    # 5. Save the AI's options to the database
    for text in generated_texts:
        new_option = GenerativeOption(
            duty_id=new_duty.duty_id,
            content_text=text,
            is_active=False # They are all false until the user selects their favorite!
        )
        db.add(new_option)
    
    db.commit()

    # 6. Return the data to the frontend
    return AIBulletResponse(
        duty_id=new_duty.duty_id,
        generated_bullets=generated_texts
    )


@router.patch("/options/{option_id}/select", status_code=status.HTTP_200_OK)
def select_generative_option(
    option_id: uuid.UUID = Path(..., description="The ID of the option the user selected"), 
    db: Session = Depends(get_db)
):
    """
    Sets the chosen AI-generated option to active and deactivates the others for that specific duty.
    """
    # 1. Find the option the user wants to select
    selected_option = db.query(GenerativeOption).filter(GenerativeOption.option_id == option_id).first()
    
    if not selected_option:
        raise HTTPException(status_code=404, detail="Generative option not found.")
    
    # 2. Find ALL options that belong to the exact same duty folder
    all_options = db.query(GenerativeOption).filter(
        GenerativeOption.duty_id == selected_option.duty_id
    ).all()
    
    # 3. Flip the switches: False for the losers, True for the winner
    for option in all_options:
        if option.option_id == option_id:
            option.is_active = True
        else:
            option.is_active = False
            
    # 4. Save the changes to the database
    db.commit()
    
    return {"message": "Option successfully selected.", "selected_option_id": option_id}
