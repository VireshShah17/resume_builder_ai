from pydantic import BaseModel
from typing import Optional
import uuid

class ResumeProjectBase(BaseModel):
    template_id: Optional[str] = "default_template"

class ResumeProjectCreate(ResumeProjectBase):
    user_id: uuid.UUID # We MUST know which user owns this resume

class ResumeProjectResponse(ResumeProjectBase):
    resume_id: uuid.UUID
    user_id: uuid.UUID

    model_config = {"from_attributes": True}