import os
import uuid
import tempfile

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    Depends
)

from fastapi.security import OAuth2PasswordRequestForm

from pydantic import BaseModel, EmailStr

from sqlalchemy.orm import Session

from database.connection import SessionLocal
from database.models import (
    User,
    Resume,
    JobRecommendation,
    SkillGap
)

from backend.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    get_db
)

from backend.resume_parser import extract_resume_text
from backend.skill_extractor import extract_skills
from backend.recommender import recommend_jobs
from backend.skill_gap import generate_skill_gap_report

from utils.preprocessing import (
    load_job_dataset,
    preprocess_job_data
)


# =====================================================
# FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title="AI Resume Analyzer API",
    description="AI-Powered Resume Analysis and Job Recommendation System",
    version="1.0"
)


# =====================================================
# REQUEST SCHEMA
# =====================================================

class RegisterRequest(BaseModel):

    name: str
    email: EmailStr
    password: str


# =====================================================
# LOAD JOB DATASET
# =====================================================

jobs = load_job_dataset("data/jobs.csv")

jobs = preprocess_job_data(jobs)


# =====================================================
# ROOT ROUTE
# =====================================================

@app.get("/")
def home():

    return {
        "message": "AI Resume Analyzer API is running!"
    }


# =====================================================
# USER REGISTRATION
# =====================================================

@app.post("/auth/register")
def register_user(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == request.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    if len(request.password) < 8:

        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 8 characters"
        )

    try:

        new_user = User(
            name=request.name,
            email=request.email,
            password_hash=hash_password(request.password)
        )

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        return {
            "message": "Registration successful",
            "user_id": new_user.user_id,
            "name": new_user.name,
            "email": new_user.email
        }

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        )


# =====================================================
# USER LOGIN
# =====================================================

@app.post("/auth/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user or not user.password_hash:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": str(user.user_id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "name": user.name
    }


# =====================================================
# USER PROFILE
# =====================================================

@app.get("/auth/me")
def get_profile(
    current_user: User = Depends(get_current_user)
):

    return {
        "user_id": current_user.user_id,
        "name": current_user.name,
        "email": current_user.email
    }


# =====================================================
# PUBLIC RESUME ANALYSIS
# NO LOGIN REQUIRED
# =====================================================

@app.post("/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...)
):

    db = SessionLocal()

    temp_path = None

    try:

        # =============================================
        # VALIDATE FILE
        # =============================================

        filename = file.filename or ""

        suffix = os.path.splitext(filename)[1].lower()

        if suffix not in [".pdf", ".docx"]:

            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are supported"
            )

        file_content = await file.read()

        if not file_content:

            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )

        # =============================================
        # SAVE TEMPORARY FILE
        # =============================================

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(file_content)

            temp_path = temp_file.name

        # =============================================
        # EXTRACT RESUME TEXT
        # =============================================

        resume_text = extract_resume_text(temp_path)

        if not resume_text or not resume_text.strip():

            raise HTTPException(
                status_code=400,
                detail="Could not extract text from resume"
            )

        # =============================================
        # EXTRACT SKILLS
        # =============================================

        skills = extract_skills(resume_text)

        # =============================================
        # GENERATE JOB RECOMMENDATIONS
        # =============================================

        recommendations = recommend_jobs(
            resume_text,
            jobs
        )

        # =============================================
        # GENERATE SKILL GAP REPORT
        # =============================================

        skill_gaps = generate_skill_gap_report(
            recommendations,
            top_n=3
        )

        # =============================================
        # CREATE GUEST USER
        # =============================================

        guest_user = User(
            name="Guest User",
            email=f"guest_{uuid.uuid4().hex}@resumeai.local",
            password_hash=None
        )

        db.add(guest_user)

        db.flush()

        # =============================================
        # SAVE RESUME
        # =============================================

        new_resume = Resume(
            user_id=guest_user.user_id,
            filename=filename,
            extracted_text=resume_text
        )

        db.add(new_resume)

        db.flush()

        # =============================================
        # SAVE JOB RECOMMENDATIONS
        # =============================================

        for job in recommendations:

            recommendation = JobRecommendation(

                resume_id=new_resume.resume_id,

                job_title=job["Job Title"],

                skill_match=float(
                    job["Skill Match"]
                ),

                semantic_similarity=float(
                    job["Semantic Similarity"]
                ),

                final_score=float(
                    job["Final Score"]
                )
            )

            db.add(recommendation)

        # =============================================
        # SAVE SKILL GAPS
        # =============================================

        skill_gap_response = []

        if isinstance(skill_gaps, dict):

            gap_items = skill_gaps.items()

        else:

            gap_items = skill_gaps

        for skill, details in gap_items:

            if isinstance(details, dict):

                frequency = details.get("frequency", 0)

                recommended_jobs = details.get(
                    "recommended_for",
                    []
                )

            else:

                frequency = 0

                recommended_jobs = details

            if isinstance(recommended_jobs, str):

                recommended_jobs = [recommended_jobs]

            recommended_for = ", ".join(
                map(str, recommended_jobs)
            )

            gap_record = SkillGap(

                resume_id=new_resume.resume_id,

                skill_name=str(skill),

                recommended_for=recommended_for
            )

            db.add(gap_record)

            skill_gap_response.append({

                "skill": str(skill),

                "frequency": frequency,

                "recommended_for": recommended_jobs

            })

        # =============================================
        # COMMIT DATABASE
        # =============================================

        db.commit()

        # =============================================
        # SUCCESS RESPONSE
        # =============================================

        return {

            "message": "Resume analyzed successfully",

            "filename": filename,

            "resume_id": new_resume.resume_id,

            "extracted_skills": skills,

            "recommendations": recommendations,

            "skill_gap_analysis": skill_gap_response,

            "database_status": "Saved successfully"

        }

    except HTTPException:

        db.rollback()

        raise

    except Exception as error:

        db.rollback()

        print("Resume Analysis Error:", str(error))

        raise HTTPException(
            status_code=500,
            detail="Resume analysis failed. Please try again."
        )

    finally:

        db.close()

        if temp_path and os.path.exists(temp_path):

            os.remove(temp_path)