"""Text cleaning and preprocessing utilities."""
import pandas as pd


def load_job_dataset(file_path):

    # Load CSV dataset
    jobs = pd.read_csv(file_path)

    return jobs


def preprocess_job_data(jobs):

    # Handle missing values
    jobs = jobs.dropna(
        subset=["job_title", "required_skills", "description"]
    ).copy()

    # Convert skills into lowercase
    jobs["required_skills"] = jobs["required_skills"].apply(
        lambda x: [skill.strip().lower() for skill in x.split("|")]
    )

    # Normalize job descriptions
    jobs["description"] = jobs["description"].str.lower()

    return jobs