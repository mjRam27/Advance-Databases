from fastapi import FastAPI, Query
from services.shared import fetch_departures

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "VBB Live Transport API"}

@app.get("/departures/{transport_type}/{station_id}")
def get_departures(
    transport_type: str,
    station_id: str,
    duration: int = Query(120, ge=1, le=240)  # optional duration parameter (default 120)
):
    return fetch_departures(station_id, transport_type, duration)
