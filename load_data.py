import pandas as pd
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='Vinmik@2508', database='skillbridge')
cursor = conn.cursor()

for file in ["data/raw/malaysia_jobs.xlsx", "data/raw/india_jobs.xlsx"]:
    df = pd.read_excel(file)
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO jobs (job_id, job_title, company, location, country, category,
                               sub_category, role_type, salary, listing_date, data_source,
                               reliability, limitation)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE job_title=VALUES(job_title)
        """, (
            str(row['Job ID']), row['Job Title'], row['Company'], row['Location'],
            row['Country'], row['Category'], row['Sub-category'], row['Role Type'],
            str(row['Salary']), str(row['Listing Date']), row['Data Source'],
            row['Reliability'], row['Limitation']
        ))

conn.commit()
print("Loaded data successfully")
conn.close()