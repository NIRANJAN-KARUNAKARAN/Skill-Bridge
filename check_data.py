import pymysql
conn = pymysql.connect(host='localhost', user='root', password='Vinmik@2508', database='skillbridge')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM jobs")
print("Total rows:", cursor.fetchone())
conn.close()