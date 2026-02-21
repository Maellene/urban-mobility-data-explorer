🚕 Urban Mobility Data Explorer

A full-stack urban mobility analytics dashboard built using Flask, MySQL, and vanilla JavaScript to explore 7.4 million NYC Yellow Taxi trips (January 2019).

🔗 Quick Links

📄 Project Report: docs/Urban Mobility System  Project Documentation.pdf

🏗 Architecture Diagram: docs/Urban Mobility System Architecture.drawio.png

📊 Team Task Sheet:
https://docs.google.com/spreadsheets/d/1y8W4NT6lLU58EVYUGtevlnCPTOuB2Ubw6QNdW0j0eJg/edit?usp=sharing

📌 Project Overview

The Urban Mobility Data Explorer analyzes large-scale taxi trip data to uncover mobility patterns across New York City.

This system:

Cleans and validates raw taxi datasets

Loads structured data into a MySQL relational database

Exposes analytics via REST APIs (Flask)

Visualizes insights using charts and tables

This project was developed for an academic assignment and runs in development mode.

🏗 System Architecture

The project follows a 3-layer architecture:

User (Browser)
        ↓
Frontend (HTML, CSS, JS, Chart.js)
        ↓ REST API Calls
Backend (Flask + Python Logic)
        ↓ SQL Queries
MySQL Database (urban_mobility)
Architecture Summary

Frontend Layer → Displays charts, filters, and trip tables

Backend Layer → Provides API endpoints and custom algorithms

Database Layer → Stores trips, zones, and rate codes

🧠 Database Design
Core Tables

trips → Fact table (7.4M records)

zones → Dimension table

ratecode → Dimension table

Relationships

zones (1) → (N) trips

ratecode (1) → (N) trips

Zones and ratecodes are indirectly related through the trips table (Star Schema model).

🛠 Tech Stack
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

```text
URBAN-MOBILITY-DATA-EXPLORER/
│
├── backend/
│   ├── data_pipeline/
│   ├── database/
│   ├── algorithm.py
│   └── main.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── logs/
│
├── docs/
│   ├── architecter diagarm.jpeg
│   └── report.pdf
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── README.md
```
🚀 Running the Backend (API)
1️⃣ Install Dependencies
pip install flask flask-cors pymysql
2️⃣ Run the Server
python main.py

You should see:

Running on http://127.0.0.1:5000

⚠️ The development server warning is normal.

✅ API Health Check

Open your browser and visit:

http://localhost:5000/api/health

Expected response:

{
  "status": "API is running"
}
📡 Available API Endpoints

/api/stats

/api/zones

/api/ratecodes

/api/trips

/api/trips-by-hour

/api/trips-by-borough

/api/trips-by-zone

/api/trips-by-ratecode

/api/top-zones-ranked

/api/trips-by-hour-custom

💻 Running the Frontend

1️⃣ Ensure backend is running on port 5000

2️⃣ Open:

frontend/index.html

OR use Live Server (port 5500).

📊 Dashboard Features
🔢 Stat Cards

Total Trips: 7,469,100

Average Fare: $12.18

Average Distance: 2.83 miles

Average Passengers: ~1.5

📈 Visualizations
Trips by Hour

Identifies peak taxi demand times.

Trips by Borough

Shows borough-level trip distribution.

Top 20 Pickup Zones

Displays the most active pickup locations.

Trips by Rate Code

Breaks down fare types.

🎟 Rate Code Meanings
Code	Meaning
1	Standard city rate
2	JFK Airport flat rate
3	Newark Airport
4	Nassau/Westchester
5	Negotiated fare
6	Group ride
🔍 Filters Section

Filters apply only to the Trip Records Table.

Available filters:

Rate Code

Results Limit

Example:

Rate Code: 2
Limit: 100

Displays 100 JFK airport trips.

📋 Trip Records Table

Displays:

Pickup & dropoff times

Passenger count

Distance

Fare amount

Pickup & dropoff zone IDs

Updates dynamically via API calls.

🔄 Data Pipeline

Raw CSV + Taxi zone shapefiles
→ Data Cleaning
→ Feature Engineering
→ Validation
→ MySQL Loading
→ REST API
→ Dashboard Visualization

👥 Collaboration Notes

Each developer must run main.py locally

localhost works only on the machine running the API

Backend and frontend must run simultaneously

📦 Final Status

✔ Database connected
✔ API returning real data
✔ 7.4M trips loaded
✔ Interactive dashboard working
✔ Documentation included

🎓 Academic Deliverables

Custom algorithm (algorithm.py)

Written report (docs/report.pdf)

Architecture diagram

README

Video walkthrough

Team task sheet

📌 Conclusion

This project demonstrates:

Large-scale data processing

Relational database modeling

REST API design

Frontend data visualization

Full-stack system integration

It showcases how backend systems, databases, and dashboards work together to analyze urban mobility at scale.
