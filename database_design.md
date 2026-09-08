## Initial Database Design (ERD)

### Entities & Fields

**Jobs**
- job_id (PK)
- original_title
- normalized_title
- country
- salary_min
- salary_max
- currency
- job_description
- posting_date
- source_id (FK → DataSources)

**Employers**
- employer_id (PK)
- name

**Locations**
- location_id (PK)
- city
- country

**Skills**
- skill_id (PK)
- skill_name (canonical)

**JobSkills** (many-to-many link table)
- job_id (FK → Jobs)
- skill_id (FK → Skills)

**DataSources**
- source_id (PK)
- source_name
- reliability_notes

### Relationships
- One Job → one Employer
- One Job → one Location
- One Job → many Skills (via JobSkills)
- One Job → one DataSource

## Database Decision
Chosen: SQLite (simple, no server setup, built into Python, ideal for a 4-week prototype)
Alternative considered: PostgreSQL (better for scale, unnecessary overhead for now)

## Backend Framework Decision
Chosen: FastAPI (auto-generates API docs, async support, fast to prototype with)
Alternative considered: Flask (simpler, but more manual setup for docs/validation)