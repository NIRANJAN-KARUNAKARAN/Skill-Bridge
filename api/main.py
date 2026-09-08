from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import Country, Job
from schemas import JobListOut, JobOut

app = FastAPI(
    title="SkillBridge API",
    description="India vs Malaysia Job-Market & Skill-Gap Platform — prototype API",
    version="0.1.0",
)


@app.get("/", tags=["meta"])
def root():
    return {"status": "ok", "service": "SkillBridge API"}


@app.get("/jobs", response_model=JobListOut, tags=["jobs"])
def list_jobs(
    country: Optional[str] = Query(None, description="e.g. Malaysia, India"),
    role: Optional[str] = Query(None, description="matches against job title"),
    category: Optional[str] = Query(None),
    min_salary: Optional[float] = Query(None, description="filter by salary_min >="),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    q = db.query(Job).options(joinedload(Job.country), joinedload(Job.source))

    if country:
        q = q.join(Country).filter(Country.country_name.ilike(country))
    if role:
        q = q.filter(
            or_(
                Job.original_title.ilike(f"%{role}%"),
                Job.normalized_title.ilike(f"%{role}%"),
            )
        )
    if category:
        q = q.filter(Job.category.ilike(f"%{category}%"))
    if min_salary is not None:
        q = q.filter(Job.salary_min >= min_salary)

    total = q.count()
    rows = q.offset(offset).limit(limit).all()

    return JobListOut(
        total=total,
        count=len(rows),
        results=[_to_job_out(r) for r in rows],
    )


@app.get("/jobs/{job_pk}", response_model=JobOut, tags=["jobs"])
def get_job(job_pk: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_pk).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return _to_job_out(job)


def _to_job_out(job: Job) -> JobOut:
    data = JobOut.model_validate(job)
    return data
