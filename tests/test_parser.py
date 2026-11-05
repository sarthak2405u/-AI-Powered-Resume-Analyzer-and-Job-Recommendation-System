from backend.resume_parser import extract_resume_text
from backend.skill_extractor import extract_skills

# Resume path
file_path = "sample_resume.pdf"

# Extract resume text
resume_text = extract_resume_text(file_path)

# Extract skills
skills = extract_skills(resume_text)

# Display results
print("\n========== EXTRACTED SKILLS ==========\n")

for category, skill_list in skills.items():

    print(f"\n{category}:")

    for skill in skill_list:
        print("-", skill)