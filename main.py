# main.py
from fastapi import FastAPI
from services.bus_service import fetch_bus_data
from services.tram_service import fetch_tram_data
from services.ice_service import fetch_ice_data
from services.sbahn_service import fetch_sbahn_data
from services.ubahn_service import fetch_ubahn_data
from services.re_service import fetch_re_data
from services.trip_service import fetch_trip_by_id
from services.refresh_service import refresh_journey
from utils.resolve import get_station_id


app = FastAPI()

@app.get("/")
def root():
    return {"message": "VBB Transport API is running!"}

@app.get("/bus")
def bus(from_station: str, to_station: str):
    print(f"📥 /bus received from {from_station} to {to_station}")

    return fetch_bus_data(from_station, to_station)

@app.get("/tram")
def tram(from_station: str, to_station: str):
    return fetch_tram_data(from_station, to_station)

@app.get("/ice")
def ice(from_station: str, to_station: str):
    return fetch_ice_data(from_station, to_station)

@app.get("/sbahn")
def sbahn(from_station: str, to_station: str):
    return fetch_sbahn_data(from_station, to_station)

@app.get("/ubahn")
def ubahn(from_station: str, to_station: str):
    return fetch_ubahn_data(from_station, to_station)

@app.get("/re")
def re(from_station: str, to_station: str):
    return fetch_re_data(from_station, to_station)

@app.get("/refresh")
def refresh(refresh_token: str):
    return refresh_journey(refresh_token)

@app.get("/trip")
def trip(trip_id: str):
    return fetch_trip_by_id(trip_id)

@app.get("/bus-name")
def bus_by_name(from_name: str, to_name: str):
    from_id = get_station_id(from_name)
    to_id = get_station_id(to_name)
    return fetch_bus_data(from_id, to_id)


