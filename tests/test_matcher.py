from backend.resume_parser import extract_resume_text
from backend.job_matcher import calculate_similarity

from utils.preprocessing import (
    load_job_dataset,
    preprocess_job_data
)


# Load resume
resume_text = extract_resume_text("sample_resume.pdf")


# Load job dataset
jobs = load_job_dataset("data/jobs.csv")

jobs = preprocess_job_data(jobs)


# Calculate similarity for each job
results = []

for index, row in jobs.iterrows():

    score = calculate_similarity(
        resume_text,
        row["description"]
    )

    results.append({
        "Job Title": row["job_title"],
        "Similarity Score": score
    })


# Sort jobs by similarity
results = sorted(
    results,
    key=lambda x: x["Similarity Score"],
    reverse=True
)


# Display recommendations
print("\n========== JOB RECOMMENDATIONS ==========\n")

for result in results:

    print(
        result["Job Title"],
        "->",
        result["Similarity Score"],
        "%"
    )