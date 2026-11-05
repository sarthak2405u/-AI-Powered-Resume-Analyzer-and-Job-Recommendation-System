from database.connection import SessionLocal

from database.models import (
    User,
    Resume,
    JobRecommendation,
    SkillGap
)


db = SessionLocal()

try:

    # Create a test user
    user = User(
        name="Test Candidate",
        email="test@example.com"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    print("User created successfully!")
    print("User ID:", user.user_id)

except Exception as error:

    db.rollback()
    print("Error:", error)

finally:

    db.close()