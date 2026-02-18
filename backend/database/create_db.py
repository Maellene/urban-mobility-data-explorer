
import pymysql

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_password"
MYSQL_DB = "urban_mobility"

def create_database():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="maellene123"
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
    conn.close()
    print("MySQL database created successfully.")

if __name__ == "__main__":
    create_database()

