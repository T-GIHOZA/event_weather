from fastapi import APIRouter, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/api/events", tags=["events"])

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")

@router.get("/{city}")
async def get_events(city: str):
    if not TICKETMASTER_API_KEY:
        raise HTTPException(status_code=500, detail="Events API key not configured")
        
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?city={city}&apikey={TICKETMASTER_API_KEY}&size=5&sort=date,asc"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Events data not found")
        data = response.json()
        
    events = []
    if "_embedded" in data and "events" in data["_embedded"]:
        for event in data["_embedded"]["events"]:
            events.append({
                "id": event.get("id"),
                "name": event.get("name"),
                "date": event.get("dates", {}).get("start", {}).get("localDate", "TBD"),
                "url": event.get("url"),
                "venue": event.get("_embedded", {}).get("venues", [{}])[0].get("name", "Unknown Venue")
            })
            
    return events
