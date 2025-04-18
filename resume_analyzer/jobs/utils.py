def calculate_match_score(required_skills, applicant_skills):
    if not required_skills or not applicant_skills:
        return 0
    required_skills_set = set(skill.lower() for skill in required_skills)
    applicant_skills_set = set(skill.lower() for skill in applicant_skills)
    matched = required_skills_set.intersection(applicant_skills_set)
    return round((len(matched) / len(required_skills_set)) * 10)