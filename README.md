# urban-mobility-data-explorer
Urban Mobility Data Explorer 

This project is a full-stack data dashboard that explores New York City taxi trips (January 2019).
It uses a Flask backend API, a MySQL database, and a vanilla HTML/CSS/JavaScript frontend to display real statistics and visualizations from 7.4 million taxi trips.

Project Overview

The Urban Mobility Data Explorer allows users to:

View overall taxi trip statistics

Explore trip patterns by time, location, and rate code

Filter and inspect individual trip records

Understand urban mobility trends through charts and tables

This project was built for an academic assignment and runs in development mode.

Tech Stack

Backend

Python

Flask

Flask-CORS

MySQL

PyMySQL

Frontend

HTML

CSS

JavaScript

Chart.js

Project Structure

URBAN-MOBILITY-DATA-EXPLORER/
│
├── backend/
│   ├── data_pipeline/
│   │   ├── clean_data.py
│   │   ├── feature_engineering.py
│   │   ├── load_data.py
│   │   ├── rejection_log.py
│   │   └── validate_data.py
│   │
│   ├── database/
│   │   ├── create_db.py
│   │   ├── create_tables.py
│   │   └── insert_cleaned_data.py
│   │
│   ├── algorithm.py
│   ├── cleaned_merged_trips.csv
│   └── main.py
│
├── data/
│   ├── logs/
│   ├── processed/
│   │
│   └── raw/
│       ├── taxi_zones/
│       │   ├── taxi_zones.dbf
│       │   ├── taxi_zones.prj
│       │   ├── taxi_zones.sbn
│       │   ├── taxi_zones.sbx
│       │   ├── taxi_zones.shp
│       │   ├── taxi_zones.shp.xml
│       │   └── taxi_zones.shx
│       │
│       ├── taxi_zone_lookup.csv
│       └── yellow_tripdata_2019-01.csv
│
├── docs/
│   ├── architecter diagram.jpeg
│   └── report.pdf
│
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
│
├── .gitignore
└── README.md

Running the Backend (API)
1. Install dependencies
pip install flask flask-cors pymysql

2. Run the server
python main.py


You should see:

Running on http://127.0.0.1:5000


⚠️ Note
You may see this warning:

WARNING: This is a development server. Do not use it in a production deployment.


This is normal and not an error.

Backend API Health Check

Open your browser and visit:

http://localhost:5000/api/health


Expected response:

{
  "status": "API is running"
}

Available API Endpoints

Once the server is running, these endpoints return real data:

/api/stats

/api/zones

/api/ratecodes

/api/trips

/api/trips-by-hour

/api/trips-by-borough

/api/trips-by-zone

/api/trips-by-ratecode


HERE IS THE LINK TO THE ARCHITECTER DIAGRAM FOR THIS PROJECT
: docs/architecter diagarm.jpeg

Running the Frontend
1. Create a frontend/ folder (if not already created)

Place these files inside it:

index.html

style.css

app.js

2. Make sure the API is running

The backend must be running on port 5000.

3. Open the frontend

Simply open index.html in your browser
(or use Live Server on port 5500).

Dashboard Features Explained (Beginner Friendly)
Stat Cards (Top Section)

Total Trips
Total number of taxi trips in January 2019 (7,469,100)

Average Fare
Average cost per taxi ride ($12.18)

Average Distance
Average trip distance in miles (2.83 miles)

Average Passengers
Average number of passengers per trip (about 1–2 people)

Charts & What They Mean
Trips by Hour of Day

Shows the busiest hours for taxis (e.g. morning and evening rush hours).

Trips by Borough

Shows which NYC boroughs generate the most taxi trips
(Manhattan usually dominates).

Top 20 Pickup Zones

Displays the top 20 locations where taxis are picked up most often
(e.g. airports, busy districts).

Trips by Rate Code

Shows how trips are distributed by fare type.

Rate Code Meanings

Code 1 — Standard city rate

Code 2 — JFK Airport flat rate

Code 3 — Newark Airport rate

Code 4 — Nassau or Westchester

Code 5 — Negotiated fare

Code 6 — Group ride

Filters Section (How It Works)

The Apply Filters button affects only the Trip Records table, not the charts.

Filters Available:

Rate Code – filters trips by fare type

Results Limit – limits how many rows are shown

Example:

If you select:

Rate Code: 2

Limit: 100

Then click Apply Filters, the table will display only 100 trips that used Rate Code 2.

Trip Records Table

This table shows individual taxi trips including:

Pickup & dropoff times

Passenger count

Distance

Fare

Pickup and dropoff zone IDs

It updates dynamically when filters are applied.

Collaboration Notes

Each frontend developer must run main.py on their own machine

localhost only works on the computer running the API

Both backend (port 5000) and frontend (port 5500 or browser) must run at the same time

Final Status

 Database connected
 API returning real data
 Frontend dashboard working
 7.4 million trips loaded

Remaining Deliverables (if required by rubric)

Custom algorithm implementation

Written report

README (this file)

Video walkthrough

Team participation sheet

Conclusion

This project successfully demonstrates how backend APIs, databases, and frontend dashboards work together to analyze and visualize large-scale urban mobility data.

BSE Team Task Sheet : 
https://docs.google.com/spreadsheets/d/1y8W4NT6lLU58EVYUGtevlnCPTOuB2Ubw6QNdW0j0eJg/edit?usp=sharing
