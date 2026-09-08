from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_id: str
    original_title: str
    normalized_title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    role_type: Optional[str] = None
    salary_raw: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None
    salary_period: Optional[str] = None
    posting_date: Optional[date] = None


class JobListOut(BaseModel):
    total: int
    count: int
    results: list[JobOut]
