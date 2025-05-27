# main.py
from fastapi import FastAPI
from services.journey_service import fetch_journey
from services.refresh_service import refresh_journey


app = FastAPI()

@app.get("/")
def root():
    return {"message": "VBB Transport API is running!"}


@app.get("/journey")
def journey(from_station: str, to_station: str):
    return fetch_journey(from_station, to_station)

@app.get("/journey/refresh")
def refresh(token: str):
    return refresh_journey(token)
