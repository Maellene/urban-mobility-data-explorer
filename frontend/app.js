const API_BASE = 'http://localhost:5000/api';

let hourChart, boroughChart, zoneChart, ratecodeChart;


let allTrips = [];

async function fetchStats() {
    const res = await fetch(`${API_BASE}/stats`);
    const data = await res.json();

    document.getElementById('total-trips').textContent = Number(data.total_trips).toLocaleString();
    document.getElementById('avg-fare').textContent = `$${data.avg_fare}`;
    document.getElementById('avg-distance').textContent = `${data.avg_distance} mi`;
    document.getElementById('avg-passengers').textContent = parseFloat(data.avg_passengers).toFixed(2);
}

async function fetchRatecodes() {
    const res = await fetch(`${API_BASE}/ratecodes`);
    const data = await res.json();
    const select = document.getElementById('ratecode-filter');

    data.forEach(r => {
        const option = document.createElement('option');
        option.value = r.ratecode_id;
        option.textContent = `Code ${r.ratecode_id}`;
        select.appendChild(option);
    });
}

async function fetchTripsByHour() {
    const res = await fetch(`${API_BASE}/trips-by-hour`);
    const data = await res.json();

    const labels = data.map(d => `${d.hour}:00`);
    const counts = data.map(d => d.trip_count);

    if (hourChart) hourChart.destroy();

    hourChart = new Chart(document.getElementById('trips-by-hour-chart'), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Trips',
                data: counts,
                backgroundColor: '#3a86ff'
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
}

async function fetchTripsByBorough() {
    const res = await fetch(`${API_BASE}/trips-by-borough`);
    const data = await res.json();

    const labels = data.map(d => d.borough);
    const counts = data.map(d => d.trip_count);

    if (boroughChart) boroughChart.destroy();

    boroughChart = new Chart(document.getElementById('trips-by-borough-chart'), {
        type: 'doughnut',
        data: {
            labels,
            datasets: [{
                data: counts,
                backgroundColor: ['#3a86ff', '#ff006e', '#fb5607', '#ffbe0b', '#8338ec']
            }]
        },
        options: { responsive: true }
    });
}

async function fetchTripsByZone() {
    const res = await fetch(`${API_BASE}/trips-by-zone`);
    const data = await res.json();

    const labels = data.map(d => d.zone_name);
    const counts = data.map(d => d.trip_count);

    if (zoneChart) zoneChart.destroy();

    zoneChart = new Chart(document.getElementById('trips-by-zone-chart'), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Trips',
                data: counts,
                backgroundColor: '#8338ec'
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { font: { size: 11 } } },
                y: { beginAtZero: true }
            }
        }
    });
}

async function fetchTripsByRatecode() {
    const res = await fetch(`${API_BASE}/trips-by-ratecode`);
    const data = await res.json();

    const labels = data.map(d => `Code ${d.ratecode_id}`);
    const counts = data.map(d => d.trip_count);

    if (ratecodeChart) ratecodeChart.destroy();

    ratecodeChart = new Chart(document.getElementById('trips-by-ratecode-chart'), {
        type: 'pie',
        data: {
            labels,
            datasets: [{
                data: counts,
                backgroundColor: ['#3a86ff', '#ff006e', '#fb5607', '#ffbe0b', '#8338ec', '#06d6a0']
            }]
        },
        options: { responsive: true }
    });
}

async function fetchTrips(filters = {}) {
    let url = `${API_BASE}/trips?limit=${filters.limit || 100}`;

    if (filters.ratecode_id) url += `&ratecode_id=${filters.ratecode_id}`;
    if (filters.pu_location_id) url += `&pu_location_id=${filters.pu_location_id}`;

    const res = await fetch(url);
    const data = await res.json();

    allTrips = data;

    const tbody = document.getElementById('trips-tbody');
    const viewMoreBtn = document.getElementById('view-more-btn');

    tbody.innerHTML = '';

    if (allTrips.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8">No records found</td></tr>';
        viewMoreBtn.style.display = 'none';
        return;
    }

    renderTrips(allTrips.slice(0, 10));

    viewMoreBtn.style.display = allTrips.length > 10 ? 'block' : 'none';
}

function renderTrips(trips) {
    const tbody = document.getElementById('trips-tbody');
    tbody.innerHTML = '';

    trips.forEach(trip => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${trip.trip_id}</td>
            <td>${trip.pickup_datetime}</td>
            <td>${trip.dropoff_datetime}</td>
            <td>${trip.passenger_count}</td>
            <td>${trip.trip_distance}</td>
            <td>$${parseFloat(trip.fare_amount).toFixed(2)}</td>
            <td>${trip.pu_location_id}</td>
            <td>${trip.do_location_id}</td>
        `;
        tbody.appendChild(row);
    });
}

document.getElementById('view-more-btn').addEventListener('click', () => {
    renderTrips(allTrips);
    document.getElementById('view-more-btn').style.display = 'none';
});

document.getElementById('apply-filters').addEventListener('click', () => {
    const ratecode_id = document.getElementById('ratecode-filter').value;
    const limit = document.getElementById('limit-filter').value;
    fetchTrips({ ratecode_id, limit });
});

async function init() {
    await fetchStats();
    await fetchRatecodes();
    await fetchTripsByHour();
    await fetchTripsByBorough();
    await fetchTripsByZone();
    await fetchTripsByRatecode();
    await fetchTrips();
}

init();