# SkillBridge Prototype — Day 3

Raw data → clean → unified schema → MySQL → API. Built against your real
`india_jobs.xlsx` / `malaysia_jobs.xlsx` (16-column format, 50 rows each).

## What this covers vs the full ERD

Day 2's A4 ERD listed 10 entities (Jobs, Employers, Locations, Countries,
Skills, Occupations, JobSkills, Users, UserSkills, DataSources,
AnalysisResults, Recommendations). This prototype implements **Jobs +
Countries + DataSources** — enough to prove the pipeline end-to-end for the
Day 3 demo. The rest can be layered on for later sprints without changing
this core.

## What's real vs. placeholder in the data

- `original_title`, `company`, `location`, `category`, `sub_category`,
  `country`, `source` — real, taken directly from your files.
- `salary_min`/`salary_max`/`currency`/`salary_period` — parsed from the raw
  salary text. India → annual INR (from "X-Y Lacs PA"), Malaysia → monthly
  MYR (from "RM X – RM Y per month"). Unparseable/undisclosed salaries are
  `NULL` (34/50 India rows say "Not disclosed" — that's real, not a bug).
- `role_type` and `posting_date` — **NULL for every row**, because both
  source files literally contain the placeholder text "Not specified/provided
  in source dataset" for every record. Worth flagging in your integration
  meeting: G1-A may need to backfill these, or the schema should mark them
  optional going forward.
- `normalized_title` — left `NULL`; that's G1-B's NLP normalization step.

## Setup (Windows PowerShell)

```powershell
cd malasiya
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

1. Install MySQL locally (or use one already running) and create the schema:

```powershell
mysql -u root -p < db\schema.sql
```

2. Copy `.env.example` to `.env` and fill in your MySQL credentials.

3. Run the ETL to clean the raw files and load them into MySQL:

```powershell
python etl\clean_and_load.py --load
```

   (Run it without `--load` first if you just want to inspect
   `data\processed\jobs_clean.csv` before touching the database.)

4. Start the API:

```powershell
cd api
uvicorn main:app --reload
```

5. Open **http://127.0.0.1:8000/docs** — FastAPI's auto-generated Swagger UI,
   good for your demo. Try:

```
GET /jobs?country=Malaysia&role=Executive
GET /jobs?country=India&min_salary=500000
GET /jobs/1
```

## Notes

- This was built and syntax-checked in a sandbox without MySQL/network
  access, so the ETL logic was verified against your real files (salary
  parsing, null handling) but the live DB load + API haven't been run
  end-to-end yet. Run steps 1–4 above and flag anything that errors.
- `job_id` + `country_id` has a unique constraint, so re-running the loader
  is safe (it upserts rather than duplicating rows).
