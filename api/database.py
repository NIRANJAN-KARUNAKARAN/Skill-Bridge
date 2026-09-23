
import os
import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return connection
    


if __name__ == "__main__":
    try:
        db = get_db_connection()
        print("✅ MySQL connected successfully!")

        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM jobs")
        count = cursor.fetchone()[0]

        print(f"✅ Jobs in database: {count}")

        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        print(f"❌ MySQL connection error: {err}")