"""Rank and recommend suitable job roles."""
from backend.skill_extractor import extract_skills
from backend.job_matcher import calculate_similarity


def calculate_skill_match(resume_skills, required_skills):

    # Flatten extracted skills
    candidate_skills = []

    for category, skills in resume_skills.items():
        candidate_skills.extend(
            [skill.lower() for skill in skills]
        )

    # Convert required skills into lowercase
    required_skills = [
        skill.lower() for skill in required_skills
    ]

    # Find matching skills
    matched_skills = list(
        set(candidate_skills) & set(required_skills)
    )

    # Calculate skill matching percentage
    if len(required_skills) == 0:
        return 0, [], required_skills

    score = (
        len(matched_skills) / len(required_skills)
    ) * 100

    return round(score, 2), matched_skills, required_skills


def recommend_jobs(resume_text, jobs):

    # Extract skills from resume
    resume_skills = extract_skills(resume_text)

    recommendations = []

    for index, row in jobs.iterrows():

        # Skill matching
        skill_score, matched, required = calculate_skill_match(
            resume_skills,
            row["required_skills"]
        )

        # Semantic similarity
        semantic_score = calculate_similarity(
            resume_text,
            row["description"]
        )

        # Combined score
        final_score = (
            (skill_score * 0.60) +
            (semantic_score * 0.40)
        )

        recommendations.append({

            "Job Title": row["job_title"],

            "Skill Match": skill_score,

            "Semantic Similarity": semantic_score,

            "Final Score": round(final_score, 2),

            "Matched Skills": matched,

            "Missing Skills": list(
                set(required) - set(matched)
            )

        })

    # Sort recommendations
    recommendations = sorted(
        recommendations,
        key=lambda x: x["Final Score"],
        reverse=True
    )

    return recommendations