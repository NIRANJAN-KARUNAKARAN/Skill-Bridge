import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="India-Malaysia Skill Bridge API")

# -------------------------
# CORS — allow the frontend (Render static site / local dev) to call this API
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your deployed frontend URL once you have it
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Load real job + skills dataset (from the India/Malaysia NLP pipeline)
# -------------------------
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "jobs_with_skills.json"
with open(DATA_PATH) as f:
    jobs = json.load(f)


class JobInput(BaseModel):
    country: str
    job_title: str
    job_description: str


@app.get("/")
def home():
    return {"message": "India-Malaysia Skill Bridge API is running"}


# -------------------------
# GET /jobs  (optional ?country=&role= filters, matches api_contract.md)
# -------------------------
@app.get("/jobs")
def get_jobs(country: Optional[str] = None, role: Optional[str] = None):
    result = jobs
    if country:
        result = [j for j in result if j["country"].lower() == country.lower()]
    if role:
        result = [j for j in result if (j["role"] or "").lower() == role.lower()]
    return result


# -------------------------
# GET /jobs/{job_id}
# -------------------------
@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    for j in jobs:
        if j["job_id"] == job_id:
            return j
    raise HTTPException(status_code=404, detail="Job not found")


# -------------------------
# GET /jobs/country/{country}  (kept for backward compatibility)
# -------------------------
@app.get("/jobs/country/{country}")
def jobs_by_country(country: str):
    result = [j for j in jobs if j["country"].lower() == country.lower()]
    return {"country": country, "count": len(result), "jobs": result}


# -------------------------
# GET /jobs/skill/{skill}
# -------------------------
@app.get("/jobs/skill/{skill}")
def jobs_by_skill(skill: str):
    result = [j for j in jobs if any(skill.lower() == s.lower() for s in j["skills"])]
    return {"skill": skill, "count": len(result), "jobs": result}


# -------------------------
# GET /skills  (optional ?role= filter, matches api_contract.md)
# -------------------------
@app.get("/skills")
def get_skills(role: Optional[str] = None):
    source = jobs
    if role:
        source = [j for j in jobs if (j["role"] or "").lower() == role.lower()]
    unique_skills = sorted({s for j in source for s in j["skills"]})
    return unique_skills


# -------------------------
# POST /extract-skills — free-text skill extraction against a simple keyword list
# -------------------------
@app.post("/extract-skills")
def extract_skills(job: JobInput):
    skill_database = sorted({s for j in jobs for s in j["skills"]})
    description = job.job_description.lower()
    detected_skills = [s for s in skill_database if s.lower() in description]
    return {"country": job.country, "job_title": job.job_title, "skills": detected_skills}


# -------------------------
# GET /match/{country}/{skill}
# -------------------------
@app.get("/match/{country}/{skill}")
def match_skill(country: str, skill: str):
    matching_jobs = [
        j for j in jobs
        if j["country"].lower() == country.lower()
        and any(skill.lower() == s.lower() for s in j["skills"])
    ]
    return {"country": country, "skill": skill, "matching_jobs": matching_jobs}
