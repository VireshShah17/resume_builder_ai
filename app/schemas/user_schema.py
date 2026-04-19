from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid


# Base properties shared across multiple schemas
class UserBase(BaseModel):
    email: EmailStr  # Pydantic will automatically validate this is a real email format!
    target_role: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None


# Properties required to create a new user via API
class UserCreate(UserBase):
    pass # Currently identical to UserBase, but keeps our architecture flexible for later


# Properties returned to the client (includes the database ID)
class UserResponse(UserBase):
    user_id: uuid.UUID

    # This config tells Pydantic it is reading a SQLAlchemy object, not a standard dictionary
    model_config = {"from_attributes": True}