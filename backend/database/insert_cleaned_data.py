import pandas as pd
import pymysql
import math
import os

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "maellene123"
MYSQL_DB = "urban_mobility"

# Read the cleaned merged CSV
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE_DIR, "cleaned_merged_trips.csv"))
df = df.where(pd.notnull(df), None)

conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB
)
cursor = conn.cursor()

# Helper functions
def safe_int(val):
    try:
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return None
        return int(val)
    except:
        return None

def safe_float(val):
    try:
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return None
        return float(val)
    except:
        return None

def safe_str(val):
    try:
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return None
        return str(val)
    except:
        return None

# Insert unique zones (pickup and dropoff)
pickup_zones = df[["PULocationID", "Borough", "Zone", "service_zone"]].drop_duplicates()
dropoff_zones = df[["DOLocationID", "Borough_dropoff", "Zone_dropoff", "service_zone_dropoff"]].drop_duplicates()
pickup_zones.columns = ["zone_id", "borough", "zone_name", "service_zone"]
dropoff_zones.columns = ["zone_id", "borough", "zone_name", "service_zone"]
all_zones = pd.concat([pickup_zones, dropoff_zones]).drop_duplicates(subset=["zone_id"])
all_zones = all_zones.where(pd.notnull(all_zones), None)

for _, row in all_zones.iterrows():
    zone_id = safe_int(row["zone_id"])
    if zone_id is not None:
        cursor.execute(
            """
            INSERT IGNORE INTO zones (zone_id, borough, zone_name, service_zone)
            VALUES (%s, %s, %s, %s)
            """,
            (zone_id, safe_str(row["borough"]), safe_str(row["zone_name"]), safe_str(row["service_zone"]))
        )

# Insert unique ratecodes
if "RatecodeID" in df.columns:
    ratecodes = df[["RatecodeID"]].drop_duplicates()
    for _, row in ratecodes.iterrows():
        ratecode_id = safe_int(row["RatecodeID"])
        if ratecode_id is not None:
            cursor.execute(
                """
                INSERT IGNORE INTO ratecode (ratecode_id, ratecode_desc)
                VALUES (%s, %s)
                """,
                (ratecode_id, "")
            )


# Insert trips in batches
batch_size = 1000
total = len(df)
for i, (_, row) in enumerate(df.iterrows()):
    cursor.execute(
        """
        INSERT INTO trips (
            pickup_datetime, dropoff_datetime, passenger_count, trip_distance, fare_amount,
            pu_location_id, do_location_id, ratecode_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            safe_str(row["tpep_pickup_datetime"]),
            safe_str(row["tpep_dropoff_datetime"]),
            safe_int(row["passenger_count"]),
            safe_float(row["trip_distance"]),
            safe_float(row["fare_amount"]),
            safe_int(row["PULocationID"]),
            safe_int(row["DOLocationID"]),
            safe_int(row["RatecodeID"])
        )
    )
    if (i + 1) % batch_size == 0:
        conn.commit()
        print(f"Inserted {i + 1:,} / {total:,} rows...")

conn.commit()
conn.close()
print("Data inserted into zones, ratecode, and trips tables.")