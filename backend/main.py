from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
from algorithm import custom_sort_zones_by_trips, custom_group_by_hour

app = Flask(__name__)
CORS(app)

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="maellene123",
        database="urban_mobility",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "API is running"})

@app.route('/api/zones', methods=['GET'])
def get_zones():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM zones")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/api/zones/borough/<borough>', methods=['GET'])
def get_zones_by_borough(borough):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM zones WHERE borough = %s", (borough,))
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/api/ratecodes', methods=['GET'])
def get_ratecodes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ratecode")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/api/trips', methods=['GET'])
def get_trips():
    conn = get_connection()
    cursor = conn.cursor()

    limit = request.args.get('limit', 100)
    pu_location_id = request.args.get('pu_location_id')
    do_location_id = request.args.get('do_location_id')
    ratecode_id = request.args.get('ratecode_id')

    query = "SELECT * FROM trips WHERE 1=1"
    params = []

    if pu_location_id:
        query += " AND pu_location_id = %s"
        params.append(pu_location_id)

    if do_location_id:
        query += " AND do_location_id = %s"
        params.append(do_location_id)

    if ratecode_id:
        query += " AND ratecode_id = %s"
        params.append(ratecode_id)

    query += " LIMIT %s"
    params.append(int(limit))

    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) as total_trips,
            ROUND(AVG(trip_distance), 2) as avg_distance,
            ROUND(AVG(fare_amount), 2) as avg_fare,
            ROUND(AVG(passenger_count), 2) as avg_passengers,
            ROUND(MAX(fare_amount), 2) as max_fare,
            ROUND(MIN(fare_amount), 2) as min_fare
        FROM trips
    """)
    data = cursor.fetchone()
    conn.close()
    return jsonify(data)

@app.route('/api/trips-by-zone', methods=['GET'])
def trips_by_zone():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT z.zone_name, z.borough, COUNT(*) as trip_count
        FROM trips t
        JOIN zones z ON t.pu_location_id = z.zone_id
        GROUP BY z.zone_name, z.borough
    """)
    data = cursor.fetchall()
    conn.close()
    sorted_data = custom_sort_zones_by_trips(data)
    return jsonify(sorted_data[:20])

@app.route('/api/trips-by-hour', methods=['GET'])
def trips_by_hour():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT HOUR(pickup_datetime) as hour, COUNT(*) as trip_count
        FROM trips
        GROUP BY HOUR(pickup_datetime)
        ORDER BY hour
    """)
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/api/trips-by-borough', methods=['GET'])
def trips_by_borough():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT z.borough, COUNT(*) as trip_count,
               ROUND(AVG(t.fare_amount), 2) as avg_fare,
               ROUND(AVG(t.trip_distance), 2) as avg_distance
        FROM trips t
        JOIN zones z ON t.pu_location_id = z.zone_id
        GROUP BY z.borough
        ORDER BY trip_count DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/api/trips-by-ratecode', methods=['GET'])
def trips_by_ratecode():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.ratecode_id, r.ratecode_desc, COUNT(*) as trip_count,
               ROUND(AVG(t.fare_amount), 2) as avg_fare
        FROM trips t
        JOIN ratecode r ON t.ratecode_id = r.ratecode_id
        GROUP BY r.ratecode_id, r.ratecode_desc
        ORDER BY trip_count DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/api/top-zones-ranked', methods=['GET'])
def top_zones_ranked():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT z.zone_name, z.borough, COUNT(*) as trip_count
        FROM trips t
        JOIN zones z ON t.pu_location_id = z.zone_id
        GROUP BY z.zone_name, z.borough
    """)
    data = cursor.fetchall()
    conn.close()
    sorted_data = custom_sort_zones_by_trips(data)
    return jsonify(sorted_data[:20])

@app.route('/api/trips-by-hour-custom', methods=['GET'])
def trips_by_hour_custom():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pickup_datetime FROM trips LIMIT 100000")
    data = cursor.fetchall()
    conn.close()
    result = custom_group_by_hour(data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)