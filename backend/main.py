from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import init_db
from .routers import weather, events

app = FastAPI(title="Event & Weather Hub")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(weather.router)
app.include_router(events.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")
