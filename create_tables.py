from database.connection import engine, Base

# Import models
from database.models import (
    User,
    Resume,
    JobRecommendation,
    SkillGap
)

# Create all database tables
Base.metadata.create_all(bind=engine)

print("All database tables created successfully!")