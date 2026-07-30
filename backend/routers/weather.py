from fastapi import APIRouter, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/api/weather", tags=["weather"])

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@router.get("/{city}")
async def get_weather(city: str):
    if not OPENWEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="Weather API key not configured")
        
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Weather data not found")
        data = response.json()
        
    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"].title(),
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }
