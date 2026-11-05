"""Extract skills and other relevant information from resume text."""
import re

# Define technical and professional skills
SKILLS = {

    "Programming Languages": [
        "Python", "Java", "C++", "C", "JavaScript", "R"
    ],

    "Web Technologies": [
        "HTML", "CSS", "JavaScript", "React", "Django",
        "Flask", "FastAPI", "Bootstrap"
    ],

    "Databases": [
        "SQL", "MySQL", "PostgreSQL", "MongoDB",
        "Oracle", "SQLite"
    ],

    "Machine Learning": [
        "Machine Learning", "Linear Regression",
        "Logistic Regression", "Decision Trees",
        "Random Forests", "KNN", "SVM",
        "Naive Bayes", "XGBoost"
    ],

    "Deep Learning": [
        "Deep Learning", "TensorFlow", "PyTorch",
        "CNN", "RNN", "Neural Networks"
    ],

    "Data Science": [
        "NumPy", "Pandas", "Matplotlib",
        "Seaborn", "Scikit-learn"
    ],

    "Cloud Technologies": [
        "AWS", "Azure", "Google Cloud",
        "Docker", "Kubernetes"
    ],

    "Soft Skills": [
        "Problem Solving", "Analytical Thinking",
        "Communication", "Teamwork",
        "Adaptability", "Time Management"
    ]
}


def extract_skills(text):

    # Normalize extracted resume text
    text = re.sub(r"\s+", " ", text)

    extracted_skills = {}

    for category, skills in SKILLS.items():

        matched_skills = []

        for skill in skills:

            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, text, re.IGNORECASE):

                matched_skills.append(skill)

        if matched_skills:

            extracted_skills[category] = matched_skills

    return extracted_skills