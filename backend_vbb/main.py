from fastapi import FastAPI, Query
from typing import Optional
from services.journey_service import fetch_journey
from services.refresh_service import refresh_journey
from utils.resolve import get_station_id
from services.departure_service import fetch_departures
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from services.station_suggestions import router as suggest_router
from services.user_history import router as user_history_router
from services.log_journey import router as log_router
from utils.db_neo4j import neo4j_conn
from services.route_service import find_shortest_route

app = FastAPI()
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["Vbb_transport"]
station_collection = db["station_logs"]

# CORS setup for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(suggest_router)
app.include_router(user_history_router)
app.include_router(log_router)


@app.on_event("startup")
async def startup_event():
    print("FastAPI is starting up...")
    
def shutdown_event():
    neo4j_conn.close()
    print("Neo4j connection closed cleanly.")


@app.get("/")
def root():
    return {"message": "VBB Transport API is running!"}


@app.get("/journey")
def journey(
    from_station: str,
    to_station: str,
    products: Optional[list[str]] = Query(default=None, alias="products[]"),
    departure: Optional[str] = None,
    user_id: Optional[str] = None
):
    from_id = get_station_id(from_station) if not from_station.isdigit() else from_station
    to_id = get_station_id(to_station) if not to_station.isdigit() else to_station
    return fetch_journey(from_id, to_id, products, departure=departure, user_id=user_id)


@app.get("/journey/refresh")
def refresh(token: str):
    return refresh_journey(token)


@app.get("/stations")
def get_stations():
    stations = list(station_collection.find({}, {"_id": 0, "station_id": 1, "name": 1}))
    return {"stations": stations}


@app.get("/departures")
def get_departures(station_id: str, duration: int = 60):
    return fetch_departures(station_id, duration)



@app.get("/route")
def get_route(start_station: str, end_station: str):
    """
    Finds the shortest route between two stations using the Neo4j graph database.
    This is ideal for your Berlin transit project[2][6].

    Example usage:
    /route?start_station=S+U Berlin Hbf&end_station=S+U Alexanderplatz
    """
    return find_shortest_route(start_station, end_station)

