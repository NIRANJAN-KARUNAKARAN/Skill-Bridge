"""
SkillBridge ETL: raw xlsx -> unified schema -> (CSV + MySQL load)

Usage:
    python clean_and_load.py                 # clean only, writes CSV
    python clean_and_load.py --load           # clean + load into MySQL

MySQL connection is read from environment variables (see .env.example):
    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
"""

import argparse
import os
import re
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

INDIA_FILE = RAW_DIR / "india_jobs.xlsx"
MALAYSIA_FILE = RAW_DIR / "malaysia_jobs.xlsx"

NOT_PROVIDED = {"not provided in source dataset", "not specified in source dataset"}


def _num(s: str):
    """Extract a float from a token like '2', '4.5', '70,000'."""
    s = s.replace(",", "").strip()
    m = re.search(r"\d+(\.\d+)?", s)
    return float(m.group()) if m else None


def parse_india_salary(raw: str):
    """
    Examples:
      '2-4 Lacs PA'            -> min=200000, max=400000, INR, annual
      '70,000-2 Lacs PA'       -> min=70000,  max=200000, INR, annual
      '50,000-1.75 Lacs PA'    -> min=50000,  max=175000, INR, annual
      'Not disclosed'          -> None, None, None, None
    """
    if not isinstance(raw, str) or raw.strip().lower() == "not disclosed":
        return None, None, None, None

    text = raw.replace("PA", "").strip()
    parts = text.split("-")
    if len(parts) != 2:
        return None, None, None, None

    values = []
    for part in parts:
        part = part.strip()
        has_lacs = "lac" in part.lower()
        n = _num(part)
        if n is None:
            return None, None, None, None
        values.append(n * 100_000 if has_lacs else n)

    return round(values[0], 2), round(values[1], 2), "INR", "annual"


def parse_malaysia_salary(raw):
    """
    Examples:
      'RM 2,800 – RM 3,500 per month'  -> min=2800, max=3500, MYR, monthly
      'MYR 4,500 - 6,000'              -> min=4500, max=6000, MYR, monthly
      NaN                              -> None, None, None, None
    """
    if not isinstance(raw, str):
        return None, None, None, None

    text = raw.replace("RM", "").replace("MYR", "").replace("per month", "")
    text = text.replace("–", "-").strip()
    parts = text.split("-")
    if len(parts) != 2:
        return None, None, None, None

    values = [_num(p) for p in parts]
    if any(v is None for v in values):
        return None, None, None, None

    return round(values[0], 2), round(values[1], 2), "MYR", "monthly"


def clean_placeholder(val):
    if isinstance(val, str) and val.strip().lower() in NOT_PROVIDED:
        return None
    return val


def load_country(path: Path, sheet: str, country: str, salary_parser) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=sheet)

    out = pd.DataFrame()
    out["job_id"] = df["Job ID"].astype(str)
    out["country"] = country
    out["original_title"] = df["Job Title"].str.strip()
    out["normalized_title"] = None  # left for G1-B's NLP normalization step
    out["company"] = df["Company"].str.strip()
    out["location"] = df["Location"].str.strip()
    out["category"] = df["Category"].str.strip()
    out["sub_category"] = df["Sub-category"].str.strip()
    out["role_type"] = df["Role Type"].apply(clean_placeholder)
    out["salary_raw"] = df["Salary"]

    parsed = df["Salary"].apply(salary_parser)
    out["salary_min"] = parsed.apply(lambda t: t[0])
    out["salary_max"] = parsed.apply(lambda t: t[1])
    out["currency"] = parsed.apply(lambda t: t[2])
    out["salary_period"] = parsed.apply(lambda t: t[3])

    out["posting_date"] = df["Listing Date"].apply(clean_placeholder)  # all NULL today
    out["source_name"] = df["Data Source"].str.strip()
    out["reliability"] = df["Reliability"].str.strip()
    out["limitation"] = df["Limitation"].str.strip()

    return out


def clean() -> pd.DataFrame:
    india = load_country(INDIA_FILE, "Updated 50 Records", "India", parse_india_salary)
    malaysia = load_country(
        MALAYSIA_FILE, "Malaysia_Job_Market_50", "Malaysia", parse_malaysia_salary
    )
    combined = pd.concat([india, malaysia], ignore_index=True)

    out_path = PROCESSED_DIR / "jobs_clean.csv"
    combined.to_csv(out_path, index=False)
    print(f"Cleaned {len(combined)} rows -> {out_path}")
    print(combined[["country", "salary_min", "salary_max", "currency", "salary_period"]]
          .groupby("country").apply(lambda g: g.notnull().mean().round(2)))
    return combined


def load_to_mysql(df: pd.DataFrame):
    import mysql.connector

    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "skillbridge"),
    )
    cur = conn.cursor()

    country_ids = {}
    for country in df["country"].unique():
        cur.execute(
            "INSERT INTO countries (country_name) VALUES (%s) "
            "ON DUPLICATE KEY UPDATE country_name=country_name",
            (country,),
        )
        cur.execute("SELECT country_id FROM countries WHERE country_name=%s", (country,))
        country_ids[country] = cur.fetchone()[0]

    source_ids = {}
    for _, row in df[["source_name", "reliability", "limitation"]].drop_duplicates(
        "source_name"
    ).iterrows():
        cur.execute(
            "INSERT INTO data_sources (source_name, reliability, limitation) "
            "VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE source_name=source_name",
            (row["source_name"], row["reliability"], row["limitation"]),
        )
        cur.execute(
            "SELECT source_id FROM data_sources WHERE source_name=%s", (row["source_name"],)
        )
        source_ids[row["source_name"]] = cur.fetchone()[0]

    insert_sql = """
        INSERT INTO jobs
            (job_id, country_id, original_title, normalized_title, company, location,
             category, sub_category, role_type, salary_raw, salary_min, salary_max,
             currency, salary_period, posting_date, source_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE original_title=VALUES(original_title)
    """
    rows = [
        (
            r.job_id, country_ids[r.country], r.original_title, r.normalized_title,
            r.company, r.location, r.category, r.sub_category, r.role_type,
            r.salary_raw, r.salary_min, r.salary_max, r.currency, r.salary_period,
            r.posting_date, source_ids[r.source_name],
        )
        for r in df.itertuples()
    ]
    cur.executemany(insert_sql, rows)
    conn.commit()
    print(f"Loaded {cur.rowcount} rows into MySQL (skillbridge.jobs)")
    cur.close()
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--load", action="store_true", help="also load into MySQL")
    args = parser.parse_args()

    cleaned = clean()
    if args.load:
        load_to_mysql(cleaned)
