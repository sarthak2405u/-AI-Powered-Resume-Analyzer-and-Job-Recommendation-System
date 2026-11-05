from utils.preprocessing import (
    load_job_dataset,
    preprocess_job_data
)

# Load dataset
jobs = load_job_dataset("data/jobs.csv")

# Process dataset
jobs = preprocess_job_data(jobs)

# Display dataset
print("\nJOB DATASET:\n")

print(jobs)

# Display available job titles
print("\nAVAILABLE JOB ROLES:\n")

print(jobs["job_title"].tolist())

# Display required skills
print("\nREQUIRED SKILLS:\n")

for index, row in jobs.iterrows():

    print(row["job_title"], ":", row["required_skills"])