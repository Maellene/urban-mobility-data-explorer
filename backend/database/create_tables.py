import sqlite3

DB_PATH = "mobility.db"

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS zones (
        zone_id INTEGER PRIMARY KEY,
        borough TEXT,
        zone_name TEXT,
        service_zone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        trip_id INTEGER PRIMARY KEY,
        pickup_datetime TEXT,
        dropoff_datetime TEXT,
        passenger_count INTEGER,
        trip_distance REAL,
        fare_amount REAL,
        pu_location_id INTEGER,
        do_location_id INTEGER,
        FOREIGN KEY (pu_location_id) REFERENCES zones(zone_id),
        FOREIGN KEY (do_location_id) REFERENCES zones(zone_id)
    )
    """)

    conn.commit()
    conn.close()

    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()

