# Event & Weather Hub

**Live Website:** http://goted.tech  
**Demo Video:** [Insert YouTube/Vimeo Link Here]

For my assignment, I decided to build a simple web app that helps you plan your day. It takes a city name and uses two external APIs to show you the current weather and a list of upcoming local events in that city. I wanted it to actually be useful instead of just another random joke generator.

## APIs Used
I used two external APIs for this project. Big thanks to their developers!
- **OpenWeather API:** [https://openweathermap.org/api](https://openweathermap.org/api) - Used to get the current weather data.
- **Ticketmaster API:** [https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/) - Used to find local events and concerts.

*Note: The API keys are hidden in a `.env` file so they don't get leaked on GitHub.*

## How to Run it Locally
If you want to test this on your own machine:

1. Clone this repository:
   ```bash
   git clone https://github.com/T-GIHOZA/event_weather.git
   cd event_weather
   ```
2. Create and start a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the main folder and add your keys:
   ```env
   OPENWEATHER_API_KEY=your_key_here
   TICKETMASTER_API_KEY=your_key_here
   ```
5. Run the backend server:
   ```bash
   uvicorn backend.main:app --reload
   ```
6. Open your browser and go to `http://127.0.0.1:8000`.

## Deployment and Load Balancer
The second part of the assignment was deploying this online using our three provided servers. 

### Web Servers (web-01 & web-02)
I put the code on both `web-01` and `web-02`. To keep the app running in the background, I set up a systemd service (`eventweather.service`) that runs the FastAPI app using Gunicorn. Then, I set up Nginx on both servers as a reverse proxy to take traffic from port 80 and send it to Gunicorn on port 8000.

### Load Balancer (lb-01)
To handle traffic distribution, I set up Nginx on the `lb-01` server to act as a Load Balancer using a Round Robin algorithm. 
I created a config file in `/etc/nginx/sites-available/loadbalancer` with this upstream block:
```nginx
upstream backend_servers {
    server 3.82.235.68;
    server 54.208.26.84;
}
```
To test that the load balancer was actually splitting the traffic, I added a custom header (`add_header X-Served-By $upstream_addr always;`) so I could use `curl -I http://goted.tech` in the terminal and watch the IP address alternate between web-01 and web-02.

## Challenges I Faced
1. **Systemd Path Errors:** When I first tried to start my background service, Gunicorn kept crashing. I checked the `journalctl` logs and realized it was because my `ExecStart` path had a typo. Git had cloned the folder as `event_weather` but I wrote `ewent_weather` in the config file. Once I fixed the folder name, it worked perfectly.
2. **Nginx Not Listening on Port 80:** When I was setting up the load balancer, external traffic wasn't going through at all. I ran `sudo netstat -tulpn | grep :80` and saw that absolutely nothing was listening on port 80. It turned out my `/etc/nginx/sites-enabled/` folder was empty because I forgot to symlink my loadbalancer config file! Once I ran the `ln -s` command and restarted Nginx, the port opened up and traffic started flowing correctly.
