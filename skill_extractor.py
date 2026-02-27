# list of common skills
skills_list = [
    "python", "java", "machine learning", "nlp",
    "sql", "tensorflow", "scikit-learn",
    "api", "backend", "data analysis"
]

# extract skills from text
def extract_skills(text):
    found_skills = []

    for skill in skills_list:
        if skill in text.lower():
            found_skills.append(skill)

    return found_skills


# find missing skills
def missing_skills(jd_skills, resume_skills):
    return list(set(jd_skills) - set(resume_skills))