from pydantic import BaseModel
from typing import Optional, List
import uuid

class ResumeProjectBase(BaseModel):
    template_id: Optional[str] = "default_template"

class ResumeProjectCreate(ResumeProjectBase):
    user_id: uuid.UUID # We MUST know which user owns this resume

class ResumeProjectResponse(ResumeProjectBase):
    resume_id: uuid.UUID
    user_id: uuid.UUID

    model_config = {"from_attributes": True}


class AIBulletRequest(BaseModel):
    resume_id: uuid.UUID
    target_role: str
    raw_input: str

class AIBulletResponse(BaseModel):
    duty_id: uuid.UUID
    generated_bullets: List[str]
