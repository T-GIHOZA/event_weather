document.getElementById('search-btn').addEventListener('click', () => {
    const city = document.getElementById('city-input').value.trim();
    if (!city) return;
    fetchData(city);
});

document.getElementById('city-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const city = e.target.value.trim();
        if (city) fetchData(city);
    }
});

async function fetchData(city) {
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const results = document.getElementById('results');
    
    loading.classList.remove('hidden');
    error.classList.add('hidden');
    results.classList.add('hidden');

    try {
        const [weatherRes, eventsRes] = await Promise.all([
            fetch(`/api/weather/${encodeURIComponent(city)}`),
            fetch(`/api/events/${encodeURIComponent(city)}`)
        ]);

        if (!weatherRes.ok || !eventsRes.ok) {
            throw new Error("Failed to fetch data. Please check the city name.");
        }

        const weatherData = await weatherRes.json();
        const eventsData = await eventsRes.json();

        renderWeather(weatherData);
        renderEvents(eventsData);

        loading.classList.add('hidden');
        results.classList.remove('hidden');

    } catch (err) {
        loading.classList.add('hidden');
        error.textContent = err.message;
        error.classList.remove('hidden');
    }
}

function renderWeather(data) {
    document.getElementById('weather-city').textContent = data.city;
    document.getElementById('weather-temp').textContent = Math.round(data.temperature);
    document.getElementById('weather-desc').textContent = data.description;
    document.getElementById('weather-humidity').textContent = data.humidity;
    document.getElementById('weather-wind').textContent = data.wind_speed;
}

function renderEvents(events) {
    const container = document.getElementById('events-list');
    container.innerHTML = '';
    
    if (events.length === 0) {
        container.innerHTML = '<p style="color: var(--text-muted)">No upcoming events found.</p>';
        return;
    }

    events.forEach(event => {
        const card = document.createElement('div');
        card.className = 'event-card';
        card.innerHTML = `
            <h3>${event.name}</h3>
            <div class="date">${event.date}</div>
            <div class="venue">${event.venue}</div>
            ${event.url ? `<a href="${event.url}" target="_blank">Tickets</a>` : ''}
        `;
        container.appendChild(card);
    });
}
