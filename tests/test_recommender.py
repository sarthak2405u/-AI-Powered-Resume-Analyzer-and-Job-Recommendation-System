from backend.resume_parser import extract_resume_text

from backend.recommender import recommend_jobs

from utils.preprocessing import (
    load_job_dataset,
    preprocess_job_data
)


# Extract resume text
resume_text = extract_resume_text("sample_resume.pdf")


# Load job dataset
jobs = load_job_dataset("data/jobs.csv")

jobs = preprocess_job_data(jobs)


# Generate recommendations
results = recommend_jobs(resume_text, jobs)


# Display results
print("\n========== AI JOB RECOMMENDATIONS ==========\n")

for result in results:

    print("\nJob Role:", result["Job Title"])

    print("Skill Match:", result["Skill Match"], "%")

    print(
        "Semantic Similarity:",
        result["Semantic Similarity"],
        "%"
    )

    print("Final Score:", result["Final Score"], "%")

    print("Matched Skills:", result["Matched Skills"])

    print("Missing Skills:", result["Missing Skills"])

    print("-" * 50)