import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os
from typing import Optional, List
from backend_vbb.utils.db_redis import cache_departure, get_cached_departure
from backend_vbb.utils.resolve import get_station_id

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vbb_transport"]
journey_collection = db["journey_logs"]
station_collection = db["station_logs"]
user_collection = db["user_logs"]

def fetch_journey(
    from_station: str,
    to_station: str,
    products: List[str],
    departure: Optional[str] = None,
    user_id: Optional[str] = None
):
    from_id = get_station_id(from_station)
    to_id = get_station_id(to_station)

    cache_key = f"{from_id}:{to_id}:{'.'.join(products or [])}:{departure or ''}"
    cached = get_cached_departure(cache_key)

    if cached:
        print("✅ Cache hit:", cache_key)
        return cached

    # API call (replace with your actual journey API logic)
    response = requests.get(
        "https://vbb.transport.api/journey",  # ⛔️ Replace with your actual endpoint
        params={
            "from": from_id,
            "to": to_id,
            "products": ','.join(products),
            "departure": departure
        }
    )
    if response.status_code != 200:
        raise Exception("Failed to fetch journey data")

    journey_data = response.json()

    # Cache response if needed
    cache_departure(cache_key, journey_data)

    # Log the journey if user_id exists
    if user_id:
        user_collection.update_one(
            {"user_id": user_id},
            {"$push": {
                "logs": {
                    "from_id": from_id,
                    "to_id": to_id,
                    "filters": products,
                    "timestamp": datetime.utcnow()
                }
            }},
            upsert=True
        )

    return journey_data
