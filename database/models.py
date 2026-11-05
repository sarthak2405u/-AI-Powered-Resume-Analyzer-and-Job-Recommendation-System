from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.connection import Base


# ==========================================
# USERS TABLE
# ==========================================

class User(Base):

    __tablename__ = "users"

    user_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String(100), nullable=False)

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    resumes = relationship(
        "Resume",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ==========================================
# RESUMES TABLE
# ==========================================

class Resume(Base):

    __tablename__ = "resumes"

    resume_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    filename = Column(
        String(255),
        nullable=False
    )

    extracted_text = Column(Text)

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="resumes"
    )

    recommendations = relationship(
        "JobRecommendation",
        back_populates="resume",
        cascade="all, delete-orphan"
    )

    skill_gaps = relationship(
        "SkillGap",
        back_populates="resume",
        cascade="all, delete-orphan"
    )


# ==========================================
# JOB RECOMMENDATIONS TABLE
# ==========================================

class JobRecommendation(Base):

    __tablename__ = "job_recommendations"

    recommendation_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    resume_id = Column(
        Integer,
        ForeignKey("resumes.resume_id"),
        nullable=False
    )

    job_title = Column(
        String(150),
        nullable=False
    )

    skill_match = Column(Float)

    semantic_similarity = Column(Float)

    final_score = Column(Float)

    resume = relationship(
        "Resume",
        back_populates="recommendations"
    )


# ==========================================
# SKILL GAPS TABLE
# ==========================================

class SkillGap(Base):

    __tablename__ = "skill_gaps"

    gap_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    resume_id = Column(
        Integer,
        ForeignKey("resumes.resume_id"),
        nullable=False
    )

    skill_name = Column(
        String(100),
        nullable=False
    )

    recommended_for = Column(
        String(150)
    )

    resume = relationship(
        "Resume",
        back_populates="skill_gaps"
    )