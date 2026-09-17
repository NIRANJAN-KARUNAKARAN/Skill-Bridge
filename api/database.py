import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="krishnasree123@",
        database="skill_bridge"
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