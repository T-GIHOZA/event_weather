# Event & Weather Hub

A web application that integrates the OpenWeather API and Ticketmaster API to allow users to search for a city and instantly see the current weather forecast alongside a list of upcoming local events.

## Architecture
- **Backend:** Python FastAPI
- **Frontend:** HTML5, JS, CSS3 (Glassmorphism UI)
- **Deployment:** Nginx Load Balancer (Round Robin) with 2 Gunicorn Web Servers.

## Environment Variables
The application strictly relies on a `.env` file to securely load API credentials without hardcoding them into the source code.
- `OPENWEATHER_API_KEY`
- `TICKETMASTER_API_KEY`

## Deployment
This project is configured to run on an AWS 3-server setup using the provided `deploy.py` automation script.

1. `web-01`: Hosts the FastAPI backend via Gunicorn
2. `web-02`: Hosts the FastAPI backend via Gunicorn
3. `lb-01`: Hosts the Nginx Load Balancer routing traffic to web-01 and web-02
