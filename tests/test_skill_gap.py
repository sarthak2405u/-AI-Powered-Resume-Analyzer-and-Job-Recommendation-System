from backend.resume_parser import extract_resume_text

from backend.recommender import recommend_jobs

from backend.skill_gap import generate_skill_gap_report

from utils.preprocessing import (
    load_job_dataset,
    preprocess_job_data
)


# Extract resume
resume_text = extract_resume_text("sample_resume.pdf")


# Load jobs
jobs = load_job_dataset("data/jobs.csv")

jobs = preprocess_job_data(jobs)


# Generate recommendations
recommendations = recommend_jobs(resume_text, jobs)


# Generate skill gap report
skill_gaps = generate_skill_gap_report(
    recommendations,
    top_n=3
)


# Display results
print("\n========== SKILL GAP ANALYSIS ==========\n")

for skill, details in skill_gaps:

    print("Missing Skill:", skill)

    print("Required in:", details["recommended_for"])

    print("Frequency:", details["count"])

    print("-" * 40)