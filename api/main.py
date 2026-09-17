from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from api.database import get_db_connection


app = FastAPI(
    title="India-Malaysia Skill Bridge API",
    description="API for job and skill matching using MySQL",
    version="1.0.0"
)


# ============================================================
# REQUEST MODELS
# ============================================================

class JobInput(BaseModel):
    job_description: str
    country: Optional[str] = None


# ============================================================
# HOME / HEALTH CHECK
# ============================================================

@app.get("/")
def home():
    return {
        "message": "India-Malaysia Skill Bridge API is running",
        "database": "MySQL"
    }


@app.get("/health")
def health_check():

    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT 1")
        cursor.fetchone()

        cursor.close()
        db.close()

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )


# ============================================================
# GET JOB COUNT
# ============================================================

@app.get("/jobs/count")
def get_job_count():

    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(*) FROM jobs")
        count = cursor.fetchone()[0]

        cursor.close()
        db.close()

        return {
            "total_jobs": count
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not get job count: {str(e)}"
        )


# ============================================================
# GET ALL SKILLS
# ============================================================

@app.get("/skills")
def get_skills():

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT skill_id, skill_name FROM skills ORDER BY skill_name"
        )

        skills = cursor.fetchall()

        cursor.close()
        db.close()

        return {
            "total_skills": len(skills),
            "skills": skills
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not get skills: {str(e)}"
        )


# ============================================================
# GET JOBS
# ============================================================

@app.get("/jobs")
def get_jobs(
    country: Optional[str] = None,
    limit: int = 20
):

    try:

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        if country:

            query = """
                SELECT
                    job_id,
                    title,
                    company_name,
                    country,
                    location,
                    experience,
                    job_description
                FROM jobs
                WHERE country = %s
                LIMIT %s
            """

            cursor.execute(query, (country, limit))

        else:

            query = """
                SELECT
                    job_id,
                    title,
                    company_name,
                    country,
                    location,
                    experience,
                    job_description
                FROM jobs
                LIMIT %s
            """

            cursor.execute(query, (limit,))

        jobs = cursor.fetchall()

        cursor.close()
        db.close()

        return {
            "total_returned": len(jobs),
            "jobs": jobs
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not get jobs: {str(e)}"
        )


# ============================================================
# GET ONE JOB
# ============================================================

@app.get("/jobs/{job_id}")
def get_job(job_id: str):

    try:

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT
                job_id,
                title,
                company_name,
                country,
                location,
                experience,
                job_description
            FROM jobs
            WHERE job_id = %s
        """

        cursor.execute(query, (job_id,))

        job = cursor.fetchone()

        cursor.close()
        db.close()

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

        return job

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not get job: {str(e)}"
        )


# ============================================================
# EXTRACT SKILLS FROM JOB DESCRIPTION
# ============================================================

@app.post("/extract-skills")
def extract_skills(job: JobInput):

    try:

        db = get_db_connection()
        cursor = db.cursor()

        # Get all skills from MySQL
        cursor.execute(
            "SELECT skill_name FROM skills"
        )

        skill_rows = cursor.fetchall()

        cursor.close()
        db.close()

        # Convert description to lowercase
        description = job.job_description.lower()

        detected_skills = []

        # Match database skills against description
        for row in skill_rows:

            skill = row[0]

            if skill and skill.lower() in description:

                detected_skills.append(skill)

        # Remove duplicates
        detected_skills = list(dict.fromkeys(detected_skills))

        return {
            "country": job.country,
            "detected_skills": detected_skills,
            "total_skills_detected": len(detected_skills)
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Skill extraction failed: {str(e)}"
        )


# ============================================================
# MATCH SKILLS TO JOBS
# ============================================================

@app.post("/match-skill")
def match_skill(job: JobInput):

    try:

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # ----------------------------------------------------
        # STEP 1: Get all skills from MySQL
        # ----------------------------------------------------

        cursor.execute(
            "SELECT skill_id, skill_name FROM skills"
        )

        skills = cursor.fetchall()

        description = job.job_description.lower()

        detected_skill_ids = []
        detected_skill_names = []

        for skill in skills:

            skill_name = skill["skill_name"]

            if skill_name and skill_name.lower() in description:

                detected_skill_ids.append(skill["skill_id"])
                detected_skill_names.append(skill_name)

        # ----------------------------------------------------
        # STEP 2: If no skills found
        # ----------------------------------------------------

        if not detected_skill_ids:

            cursor.close()
            db.close()

            return {
                "detected_skills": [],
                "total_matching_jobs": 0,
                "jobs": []
            }

        # ----------------------------------------------------
        # STEP 3: Find jobs containing those skills
        # ----------------------------------------------------

        placeholders = ",".join(
            ["%s"] * len(detected_skill_ids)
        )

        query = f"""
            SELECT
                j.job_id,
                j.title,
                j.company_name,
                j.country,
                j.location,
                j.experience,
                COUNT(DISTINCT js.skill_id) AS matched_skills
            FROM jobs j
            JOIN job_skills js
                ON j.job_id = js.job_id
            WHERE js.skill_id IN ({placeholders})
        """

        parameters = detected_skill_ids

        # Optional country filter
        if job.country:

            query += """
                AND j.country = %s
            """

            parameters = detected_skill_ids + [job.country]

        query += """
            GROUP BY
                j.job_id,
                j.title,
                j.company_name,
                j.country,
                j.location,
                j.experience
            ORDER BY matched_skills DESC
            LIMIT 20
        """

        cursor.execute(
            query,
            parameters
        )

        matching_jobs = cursor.fetchall()

        cursor.close()
        db.close()

        # ----------------------------------------------------
        # STEP 4: Return result
        # ----------------------------------------------------

        return {
            "detected_skills": detected_skill_names,
            "total_matching_jobs": len(matching_jobs),
            "jobs": matching_jobs
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Job matching failed: {str(e)}"
        )