import sqlite3

conn = sqlite3.connect("data/processed/skillbridge.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Jobs (
    job_id INTEGER PRIMARY KEY,
    original_title TEXT,
    normalized_title TEXT,
    country TEXT,
    salary_min REAL,
    salary_max REAL,
    currency TEXT,
    job_description TEXT,
    posting_date TEXT,
    source_id INTEGER
)
""")

conn.commit()
conn.close()
print("Database created successfully.")