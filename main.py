# main.py
from fastapi import FastAPI, Query
from services.journey_service import fetch_journey
from services.refresh_service import refresh_journey
from utils.resolve import get_station_id  # Optional, only if using names instead of IDs

app = FastAPI()

@app.get("/")
def root():
    return {"message": "VBB Transport API is running!"}

@app.get("/journey")
def journey(
    from_station: str,
    to_station: str,
    products: list[str] = Query(default=None)
):
    from_id = get_station_id(from_station) if not from_station.isdigit() else from_station
    to_id = get_station_id(to_station) if not to_station.isdigit() else to_station
    return fetch_journey(from_id, to_id, products)

@app.get("/journey/refresh")
def refresh(token: str):
    return refresh_journey(token)
