def generate_skill_gap_report(recommendations, top_n=3):

    # Consider top recommended jobs
    top_jobs = recommendations[:top_n]

    skill_frequency = {}

    for job in top_jobs:

        missing_skills = job["Missing Skills"]

        for skill in missing_skills:

            if skill not in skill_frequency:

                skill_frequency[skill] = {
                    "count": 0,
                    "recommended_for": []
                }

            skill_frequency[skill]["count"] += 1

            skill_frequency[skill]["recommended_for"].append(
                job["Job Title"]
            )

    # Sort skills by frequency
    sorted_skills = sorted(
        skill_frequency.items(),
        key=lambda x: x[1]["count"],
        reverse=True
    )

    return sorted_skills