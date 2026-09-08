import pymysql

conn = pymysql.connect(host='localhost', user='root', password='Vinmik@2508')
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS skillbridge")
cursor.execute("USE skillbridge")

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    job_id VARCHAR(50) PRIMARY KEY,
    job_title VARCHAR(255),
    company VARCHAR(255),
    location VARCHAR(255),
    country VARCHAR(100),
    category VARCHAR(100),
    sub_category VARCHAR(100),
    role_type VARCHAR(100),
    salary VARCHAR(100),
    listing_date VARCHAR(100),
    data_source VARCHAR(100),
    reliability TEXT,
    limitation TEXT
)
""")

print("Database and table created successfully")
conn.commit()
conn.close()