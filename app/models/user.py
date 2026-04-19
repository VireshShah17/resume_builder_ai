# Import required libraries
import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4, index = True)
    email = Column(String, unique = True, index = True, nullable = False)
    target_role = Column(String, nullable = True)
    linkedin_url = Column(String, nullable = True)
    github_url = Column(String, nullable = True)


    # Relationships
    resumes = relationship("ResumeProject", back_populates = "owner", cascade = "all, delete-orphan")
