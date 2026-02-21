# Urban Mobility Data Explorer

A full-stack urban mobility analytics dashboard built with Flask, MySQL, and vanilla JavaScript, analyzing 7.4 million NYC Yellow Taxi trips from January 2019.

---

## Quick Links

- [Project Report]([docs/Urban%20Mobility%20System%20Project%20Documentation.pdf](https://github.com/Maellene/urban-mobility-data-explorer/blob/main/docs/Urban%20Mobility%20System%20%20Project%20Documentation.pdf))
- [Architecture Diagram](https://github.com/Maellene/urban-mobility-data-explorer/blob/main/docs/Urban%20Mobility%20System%20Architecture.drawio.png)
- [Team Task Sheet](https://docs.google.com/spreadsheets/d/1y8W4NT6lLU58EVYUGtevlnCPTOuB2Ubw6QNdW0j0eJg/edit?usp=sharing)
- [Demo Video](https://youtu.be/X40WW9D0GZc)) 

---

## Overview

The Urban Mobility Data Explorer analyzes large-scale taxi trip data to uncover mobility patterns across New York City. The system cleans and validates raw taxi datasets, loads structured data into a MySQL relational database, exposes analytics via REST APIs built with Flask, and visualizes insights through an interactive dashboard.

---

## System Architecture

The project follows a three-layer architecture:

```
User (Browser)
      ↓
Frontend (HTML, CSS, JS, Chart.js)
      ↓  REST API Calls
Backend (Flask + Python Logic)
      ↓  SQL Queries
MySQL Database (urban_mobility)
```

- **Frontend Layer** — Displays charts, filters, and trip tables
- **Backend Layer** — Provides API endpoints and custom algorithms
- **Database Layer** — Stores trips, zones, and rate codes

---

## Database Design

**Core Tables**

| Table      | Type      | Description                  |
|------------|-----------|------------------------------|
| `trips`    | Fact      | 7.4M trip records            |
| `zones`    | Dimension | NYC taxi zone definitions    |
| `ratecode` | Dimension | Fare type definitions        |

The schema follows a **Star Model**: `zones` and `ratecode` both relate to `trips`, and are indirectly related to each other through it.

---

## Tech Stack

**Backend:** Python, Flask, Flask-CORS, MySQL, PyMySQL

**Frontend:** HTML, CSS, JavaScript, Chart.js

---

## Project Structure

```
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
│   ├── architecture_diagram.png
│   └── report.pdf
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── README.md
```

---

## Getting Started

### 1. Install Dependencies

```bash
pip install flask flask-cors pymysql
```

### 2. Start the Backend

```bash
python main.py
```

The server will run at `http://127.0.0.1:5000`. The development server warning is expected.

### 3. Verify the API

Open your browser and visit:

```
http://localhost:5000/api/health
```

Expected response:

```json
{
  "status": "API is running"
}
```

### 4. Launch the Frontend

Ensure the backend is running on port 5000, then open `frontend/index.html` directly in your browser, or serve it via Live Server on port 5500.

---

## API Endpoints

| Endpoint                    | Description                          |
|-----------------------------|--------------------------------------|
| `/api/stats`                | Summary statistics                   |
| `/api/zones`                | All zone records                     |
| `/api/ratecodes`            | All rate code records                |
| `/api/trips`                | Trip records (filterable)            |
| `/api/trips-by-hour`        | Trip volume grouped by hour          |
| `/api/trips-by-borough`     | Trip volume grouped by borough       |
| `/api/trips-by-zone`        | Trip volume grouped by zone          |
| `/api/trips-by-ratecode`    | Trip volume grouped by rate code     |
| `/api/top-zones-ranked`     | Top 20 pickup zones                  |
| `/api/trips-by-hour-custom` | Custom hourly trip query             |

---

## Dashboard Features

**Stat Cards**

- Total Trips: 7,469,100
- Average Fare: $12.18
- Average Distance: 2.83 miles
- Average Passengers: ~1.5

**Charts**

- **Trips by Hour** — Identifies peak taxi demand times
- **Trips by Borough** — Borough-level trip distribution
- **Top 20 Pickup Zones** — Most active pickup locations
- **Trips by Rate Code** — Breakdown of fare types

**Filters**

Filters apply to the Trip Records Table only. Available options: Rate Code, Results Limit.

Example: setting Rate Code to `2` and Limit to `100` returns 100 JFK airport trips.

**Trip Records Table**

Displays pickup/dropoff times, passenger count, distance, fare amount, and pickup/dropoff zone IDs. Updates dynamically via API.

---

## Rate Code Reference

| Code | Meaning               |
|------|-----------------------|
| 1    | Standard city rate    |
| 2    | JFK Airport flat rate |
| 3    | Newark Airport        |
| 4    | Nassau/Westchester    |
| 5    | Negotiated fare       |
| 6    | Group ride            |

---

## Data Pipeline

```
Raw CSV + Taxi Zone Shapefiles
  → Data Cleaning
  → Feature Engineering
  → Validation
  → MySQL Loading
  → REST API
  → Dashboard Visualization
```

---

## Running Locally — Team Notes

- Each developer must run `main.py` on their own machine
- `localhost` is only accessible on the machine running the API
- The backend and frontend must run simultaneously

---

## Academic Deliverables

- Custom algorithm (`algorithm.py`)
- Written report (`docs/report.pdf`)
- Architecture diagram
- README
- Video walkthrough
- Team task sheet

---

## Project Status

| Component              | Status |
|------------------------|--------|
| Database connected     | Done   |
| API returning real data| Done   |
| 7.4M trips loaded      | Done   |
| Interactive dashboard  | Done   |
| Documentation          | Done   |

---

## Conclusion

This project demonstrates large-scale data processing, relational database modeling, REST API design, and frontend data visualization — showing how backend systems, databases, and dashboards work together to analyze urban mobility at scale.
