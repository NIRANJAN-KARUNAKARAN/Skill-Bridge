from fastapi import FastAPI
import pymysql

app = FastAPI()

@app.get("/jobs")
def get_jobs(country: str = None):
    conn = pymysql.connect(host='localhost', user='root', password='Vinmik@2508', database='skillbridge')
    cursor = conn.cursor()
    if country:
        cursor.execute("SELECT * FROM jobs WHERE country = %s", (country,))
    else:
        cursor.execute("SELECT * FROM jobs")
    columns = [desc[0] for desc in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return rows