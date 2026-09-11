from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
from models import Job, Country, DataSource

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="India-Malaysia Skill Bridge API",
    version="1.0.0",
    description="Skills data aggregation API for India and Malaysia job markets"
)

# -------------------------
# CORS — allow the frontend to call this API
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your deployed frontend URL once you have it
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    """Database session dependency for all endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================
# HEALTH CHECK & ROOT
# =========================================
@app.get("/")
def health_check():
    """API health check endpoint"""
    return {
        "status": "running",
        "message": "India-Malaysia Skill Bridge API is operational",
        "version": "1.0.0"
    }


# =========================================
# JOBS ENDPOINTS
# =========================================

@app.get("/jobs")
def get_jobs(
    country: Optional[str] = None,
    role: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all jobs with optional filtering by country and role.
    
    Query Parameters:
    - country: Filter by country (e.g., "India", "Malaysia")
    - role: Filter by normalized job title/role
    - skip: Pagination offset (default: 0)
    - limit: Number of results (default: 100, max: 1000)
    
    Returns: List of jobs matching the criteria
    """
    query = db.query(Job)
    
    if country:
        # Join with Country table for filtering
        query = query.join(Country).filter(Country.country_name.ilike(f"%{country}%"))
    
    if role:
        query = query.filter(Job.normalized_title.ilike(f"%{role}%"))
    
    total = query.count()
    jobs = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "count": len(jobs),
        "skip": skip,
        "limit": limit,
        "results": jobs
    }


@app.get("/jobs/{job_id}")
def get_job_by_id(job_id: str, db: Session = Depends(get_db)):
    """
    Get a single job by its ID.
    
    Path Parameters:
    - job_id: The job ID to retrieve
    
    Returns: Single job object or 404 if not found
    """
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with ID '{job_id}' not found")
    return job


@app.get("/jobs/country/{country}")
def jobs_by_country(country: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all jobs in a specific country.
    
    Path Parameters:
    - country: Country name (e.g., "India", "Malaysia")
    
    Returns: Count and list of jobs in that country
    """
    query = db.query(Job).join(Country).filter(Country.country_name.ilike(country))
    total = query.count()
    jobs = query.offset(skip).limit(limit).all()
    
    return {
        "country": country,
        "total": total,
        "count": len(jobs),
        "jobs": jobs
    }


# =========================================
# SKILLS ENDPOINTS
# =========================================

@app.get("/skills")
def get_all_skills(db: Session = Depends(get_db)):
    """
    Get all unique skills across all jobs.
    
    Note: Skills are extracted from job descriptions and stored in the 
    normalized_title or category fields. This endpoint returns unique 
    skill terms found in the dataset.
    
    Returns: List of unique skills (sorted alphabetically)
    """
    # Extract unique categories as proxies for "skills"
    # (In full implementation, you'd have a dedicated Skills table)
    skills = db.query(Job.category).distinct().filter(Job.category.isnot(None)).all()
    unique_skills = sorted([s[0] for s in skills if s[0]])
    
    return {
        "total": len(unique_skills),
        "skills": unique_skills
    }


@app.get("/skills/by-role/{role}")
def skills_by_role(role: str, db: Session = Depends(get_db)):
    """
    Get skills associated with a specific role/job title.
    
    Path Parameters:
    - role: The job role (e.g., "Data Scientist", "Developer")
    
    Returns: List of skills commonly associated with this role
    """
    # Query jobs matching the role and extract unique skills (categories)
    jobs = db.query(Job).filter(Job.normalized_title.ilike(f"%{role}%")).all()
    skills = sorted(set(j.category for j in jobs if j.category))
    
    return {
        "role": role,
        "job_count": len(jobs),
        "skills": skills
    }


# =========================================
# MATCHING & CROSS-COUNTRY ANALYSIS
# =========================================

@app.get("/match/{country}/{skill}")
def match_skill_in_country(
    country: str,
    skill: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Find jobs in a specific country that require a specific skill.
    
    Path Parameters:
    - country: Country name (e.g., "India", "Malaysia")
    - skill: Skill name (e.g., "Python", "SQL")
    
    Returns: Matching jobs with salary and details
    """
    query = db.query(Job).join(Country).filter(
        Country.country_name.ilike(country),
        Job.category.ilike(f"%{skill}%")
    )
    
    total = query.count()
    jobs = query.offset(skip).limit(limit).all()
    
    return {
        "country": country,
        "skill": skill,
        "total": total,
        "count": len(jobs),
        "jobs": jobs
    }


@app.get("/salary-stats/{country}")
def salary_stats(country: str, db: Session = Depends(get_db)):
    """
    Get salary statistics for a country.
    
    Path Parameters:
    - country: Country name (e.g., "India", "Malaysia")
    
    Returns: Min, max, average salaries and currency information
    """
    from sqlalchemy import func
    
    stats = db.query(
        func.min(Job.salary_min).label("min_salary"),
        func.max(Job.salary_max).label("max_salary"),
        func.avg(Job.salary_min).label("avg_min_salary"),
        func.avg(Job.salary_max).label("avg_max_salary"),
        Job.currency,
        Job.salary_period
    ).join(Country).filter(
        Country.country_name.ilike(country)
    ).group_by(Job.currency, Job.salary_period).first()
    
    if not stats:
        raise HTTPException(status_code=404, detail=f"No salary data found for {country}")
    
    return {
        "country": country,
        "salary_min": float(stats[0]) if stats[0] else None,
        "salary_max": float(stats[1]) if stats[1] else None,
        "avg_min_salary": float(stats[2]) if stats[2] else None,
        "avg_max_salary": float(stats[3]) if stats[3] else None,
        "currency": stats[4],
        "salary_period": stats[5]
    }


# =========================================
# DATA SOURCE TRACKING
# =========================================

@app.get("/sources")
def get_data_sources(db: Session = Depends(get_db)):
    """
    Get all data sources and their reliability information.
    
    Returns: List of sources with reliability notes and limitations
    """
    sources = db.query(DataSource).all()
    
    return {
        "total": len(sources),
        "sources": sources
    }


@app.get("/jobs/source/{source_id}")
def jobs_by_source(source_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all jobs from a specific data source.
    
    Path Parameters:
    - source_id: The data source ID
    
    Returns: Jobs from that source with source metadata
    """
    source = db.query(DataSource).filter(DataSource.source_id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail=f"Data source {source_id} not found")
    
    query = db.query(Job).filter(Job.source_id == source_id)
    total = query.count()
    jobs = query.offset(skip).limit(limit).all()
    
    return {
        "source": {
            "id": source.source_id,
            "name": source.source_name,
            "reliability": source.reliability,
            "limitation": source.limitation
        },
        "total": total,
        "count": len(jobs),
        "jobs": jobs
    }


# =========================================
# ANALYTICS & INSIGHTS
# =========================================

@app.get("/stats/country-summary")
def country_summary(db: Session = Depends(get_db)):
    """
    Get high-level statistics for each country.
    
    Returns: Job counts, salary ranges, and data quality metrics per country
    """
    from sqlalchemy import func
    
    stats = db.query(
        Country.country_name,
        func.count(Job.id).label("job_count"),
        func.count(Job.salary_min).label("jobs_with_salary"),
        func.avg(Job.salary_min).label("avg_min_salary"),
        func.avg(Job.salary_max).label("avg_max_salary"),
        Job.currency
    ).join(Job).group_by(Country.country_id, Country.country_name, Job.currency).all()
    
    return {
        "countries": [
            {
                "country": s[0],
                "total_jobs": s[1],
                "jobs_with_salary": s[2],
                "avg_min_salary": float(s[3]) if s[3] else None,
                "avg_max_salary": float(s[4]) if s[4] else None,
                "currency": s[5]
            }
            for s in stats
        ]
    }


# =========================================
# ERROR HANDLERS
# =========================================

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    return {
        "error": "Internal Server Error",
        "message": str(exc),
        "status_code": 500
    }
