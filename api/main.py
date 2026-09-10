from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="India-Malaysia Skill Bridge API")


# -------------------------
# Sample Job Data
# -------------------------

jobs = [
    {
        "id": 1,
        "country": "Malaysia",
        "job_title": "Software Engineer",
        "company": "Tech Malaysia",
        "skills": ["Python", "SQL", "Git", "REST API"]
    },
    {
        "id": 2,
        "country": "Malaysia",
        "job_title": "Data Analyst",
        "company": "Data Solutions MY",
        "skills": ["Python", "SQL", "Excel", "Power BI"]
    },
    {
        "id": 3,
        "country": "India",
        "job_title": "Software Developer",
        "company": "Tech India",
        "skills": ["Python", "Java", "SQL", "Git"]
    },
    {
        "id": 4,
        "country": "India",
        "job_title": "Data Scientist",
        "company": "Analytics India",
        "skills": ["Python", "Machine Learning", "SQL", "Pandas"]
    }
]


# -------------------------
# Request Model
# -------------------------

class JobInput(BaseModel):
    country: str
    job_title: str
    job_description: str


# -------------------------
# Home API
# -------------------------

@app.get("/")
def home():
    return {
        "message": "India-Malaysia Skill Bridge API is running"
    }


# -------------------------
# Get all jobs
# -------------------------

@app.get("/jobs")
def get_jobs():
    return jobs


# -------------------------
# Search by country
# -------------------------

@app.get("/jobs/country/{country}")
def jobs_by_country(country: str):

    result = [
        job for job in jobs
        if job["country"].lower() == country.lower()
    ]

    return {
        "country": country,
        "count": len(result),
        "jobs": result
    }


# -------------------------
# Search by skill
# -------------------------

@app.get("/jobs/skill/{skill}")
def jobs_by_skill(skill: str):

    result = []

    for job in jobs:
        if any(skill.lower() == s.lower() for s in job["skills"]):
            result.append(job)

    return {
        "skill": skill,
        "count": len(result),
        "jobs": result
    }


# -------------------------
# Extract skills from job
# -------------------------

@app.post("/extract-skills")
def extract_skills(job: JobInput):

    skill_database = [
        "Python",
        "Java",
        "C++",
        "SQL",
        "Git",
        "REST API",
        "Excel",
        "Power BI",
        "Machine Learning",
        "Pandas",
        "HTML",
        "CSS",
        "JavaScript"
    ]

    description = job.job_description.lower()

    detected_skills = []

    for skill in skill_database:
        if skill.lower() in description:
            detected_skills.append(skill)

    return {
        "country": job.country,
        "job_title": job.job_title,
        "skills": detected_skills
    }


# -------------------------
# Skill matching
# -------------------------

@app.get("/match/{country}/{skill}")
def match_skill(country: str, skill: str):

    matching_jobs = []

    for job in jobs:

        if job["country"].lower() == country.lower():

            if any(skill.lower() == s.lower()
                   for s in job["skills"]):

                matching_jobs.append(job)

    return {
        "country": country,
        "skill": skill,
        "matching_jobs": matching_jobs
    }