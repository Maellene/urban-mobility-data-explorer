import sqlite3

DB_PATH = "mobility.db"

def create_database():
    conn = sqlite3.connect(DB_PATH)
    conn.close()
    print("Database created successfully.")

if __name__ == "__main__":
    create_database()

