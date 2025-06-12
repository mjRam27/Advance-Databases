import os
import sys
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pymongo import MongoClient
from typing import Optional, List

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.journey_service import fetch_journey
from services.refresh_service import refresh_journey
from utils.resolve import get_station_id
from utils.db_redis import cache_departure, get_cached_departure

# 🔄 Load environment variables
load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vbb_transport"]
station_collection = db["station_logs"]

# 🌐 Journey Endpoint
@app.get("/journey")
def journey(
    from_station: str,
    to_station: str,
    products: Optional[List[str]] = Query(default=None, alias="products[]"),
    departure: Optional[str] = None,
    user_id: Optional[str] = None
):
    # Safety for null products
    products = products or []

    # Convert to station IDs
    from_id = get_station_id(from_station)
    to_id = get_station_id(to_station)

    return fetch_journey(
        from_station=from_station,
        to_station=to_station,
        products=products,
        departure=departure,
        user_id=user_id
    )

# 🔁 Optional Refresh Endpoint (if needed)
@app.get("/journey/refresh")
def refresh(token: str):
    return refresh_journey(token)

# ✅ Health Check
@app.get("/")
def health():
    return {"message": "API is working 🚀"}
