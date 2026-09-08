## API Contract — G2-A

### Endpoints

**GET /jobs**
Returns all job listings.

**GET /jobs/{id}**
Returns a single job by job_id.

**GET /jobs?country=Malaysia**
Returns all jobs filtered by country.

**GET /jobs?country=Malaysia&role=Data%20Scientist**
Returns jobs filtered by country and normalized_title.

**GET /skills?role=Data%20Scientist**
Returns the skills associated with a given role.

### Example Request & Response

Request:
GET /jobs?country=Malaysia&role=Data%20Scientist

Response:
{
  "job_id": 1001,
  "job_title": "Data Scientist",
  "country": "Malaysia",
  "salary_min": 5000,
  "salary_max": 8000,
  "currency": "MYR",
  "posting_date": "2026-09-01",
  "skills": ["Python", "SQL", "Machine Learning"]
}