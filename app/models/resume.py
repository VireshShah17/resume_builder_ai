# Import required libraries
import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class SectionType(enum.Enum):
    SUMMARY = "Summary"
    EXPERIENCE = "Experience"
    PROJECT = "Project"
    SKILLS = "Skills"
    CERTIFICATIONS = "Certifications"
    ACHIEVEMENTS = "Achievements"
    EDUCATION = "Education"


class ResumeProject(Base):
    __tablename__ = "resume_projects"

    resume_id = Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4, index = True)
    user_id = Column(UUID(as_uuid = True), ForeignKey("user_profiles.user_id"), nullable = False)
    template_id = Column(String, nullable = True) 

    # Relationships
    owner = relationship("UserProfile", back_populates = "resumes")
    sections = relationship("ResumeSection", back_populates = "resume", cascade = "all, delete-orphan")


class ResumeSection(Base):
    __tablename__ = "resume_sections"

    section_id = Column(UUID(as_uuid =True), primary_key=True, default=uuid.uuid4, index=True)
    resume_id = Column(UUID(as_uuid = True), ForeignKey("resume_projects.resume_id"), nullable = False)
    section_type = Column(Enum(SectionType), nullable = False)
    display_order = Column(Integer, default = 0)

    # Relationships
    resume = relationship("ResumeProject", back_populates = "sections")
    experience_duties = relationship("ExperienceDuty", back_populates = "section", cascade = "all, delete-orphan")


class ExperienceDuty(Base):
    __tablename__ = "experience_duties"

    duty_id = Column(UUID(as_uuid =True), primary_key=True, default=uuid.uuid4, index=True)
    section_id = Column(UUID(as_uuid = True), ForeignKey("resume_sections.section_id"), nullable = False)
    raw_input = Column(Text, nullable = True) # The user's initial brain dump

    # Relationships
    section = relationship("ResumeSection", back_populates = "experience_duties")
    generative_options = relationship("GenerativeOption", back_populates = "duty", cascade = "all, delete-orphan")


class GenerativeOption(Base):
    __tablename__ = "generative_options"

    option_id = Column(UUID(as_uuid = True), primary_key=True, default=uuid.uuid4, index=True)
    duty_id = Column(UUID(as_uuid = True), ForeignKey("experience_duties.duty_id"), nullable = False)
    content_text = Column(Text, nullable = False) # The AI generated text
    is_active = Column(Boolean, default = False)  # True when the user selects this option

    # Relationships
    duty = relationship("ExperienceDuty", back_populates = "generative_options")
