import pymysql

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "maellene123"
MYSQL_DB = "urban_mobility"

def create_tables():
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
    )
    cursor = conn.cursor()

    # Create zones table 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS zones (
        zone_id INT PRIMARY KEY,
        borough VARCHAR(255),
        zone_name VARCHAR(255),
        service_zone VARCHAR(255)
    )
    """)

    # Create ratecode table 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ratecode (
        ratecode_id INT PRIMARY KEY,
        ratecode_desc VARCHAR(255)
    )
    """)

    # Create trips table 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        trip_id INT PRIMARY KEY AUTO_INCREMENT,
        pickup_datetime DATETIME,
        dropoff_datetime DATETIME,
        passenger_count INT,
        trip_distance FLOAT,
        fare_amount FLOAT,
        pu_location_id INT,
        do_location_id INT,
        ratecode_id INT,
        FOREIGN KEY (pu_location_id) REFERENCES zones(zone_id),
        FOREIGN KEY (do_location_id) REFERENCES zones(zone_id),
        FOREIGN KEY (ratecode_id) REFERENCES ratecode(ratecode_id)
    )
    """)

    conn.commit()
    conn.close()

    print("MySQL tables created successfully.")

if __name__ == "__main__":
    create_tables()

