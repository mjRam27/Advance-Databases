import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os
from utils.db_redis import cache_departure, get_cached_departure
from utils.resolve import get_station_id  # Ensure this is available

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["Vbb_transport"]
journey_collection = db["journey_logs"]
station_collection = db["station_logs"]
user_collection = db["user_logs"]

def fetch_journey(from_station: str, to_station: str, products: list[str] = None, date: str = None, user_id: str = None, departure: str = None):
    # ✅ Resolve station names to IDs if needed
    from_id = get_station_id(from_station) if not from_station.isdigit() else from_station
    to_id = get_station_id(to_station) if not to_station.isdigit() else to_station

    # ✅ Build Redis cache key
    cache_key = f"{from_id}:{to_id}:{','.join(products or [])}:{date or ''}"
    cached = get_cached_departure(cache_key)
    if cached:
        print("✅ Cache hit:", cache_key)
        return {"status": "cached", "journey": cached}

    # Call VBB API
    url = "https://v5.vbb.transport.rest/journeys"
    params = {
        "from": from_id,
        "to": to_id,
        "stopovers": True,
        "results": 5,
        "language": "en",
        "duration":60,
        "departure": departure ,
    }

    if products:
        for p in products:
            params.setdefault("products[]", []).append(p)

    if date:
        params["departure"] = date  # ISO 8601 datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("journeys"):
            return {"status": "error", "message": "No journey found"}

        journey = data["journeys"][0]
        leg = journey["legs"][0]

        stops = [
            {
                "stop": s["stop"]["name"],
                "station_id": s["stop"]["id"],
                "departure": s.get("departure"),
                "arrival": s.get("arrival"),
                "platform": s.get("platform"),
                "plannedPlatform": s.get("plannedPlatform"),
                "delay": s.get("departureDelay", 0)
            }
            for s in leg.get("stopovers", [])
        ]

        entry = {
            "from": leg["origin"]["name"],
            "to": leg["destination"]["name"],
            "line": leg.get("line", {}).get("name"),
            "mode": leg.get("line", {}).get("mode"),
            "platform": leg.get("platform"),
            "delay": leg.get("departureDelay", 0),
            "timestamp": datetime.utcnow().isoformat(),
            "stops": stops,
            "user_id": user_id  # ✅ Optional user tracking
        }

        # Save to MongoDB
        result = journey_collection.insert_one(entry)
        entry["_id"] = str(result.inserted_id)

        # Update station logs
        for s in stops:
            station_collection.update_one(
                {"station_id": s["station_id"]},
                {"$set": {
                    "name": s["stop"],
                    "platform": s["platform"],
                    "line": leg.get("line", {}).get("name")
                }},
                upsert=True
            )

        # Log per user (if needed)
        if user_id:
            user_collection.insert_one({
                "user_id": user_id,
                "from": leg["origin"]["name"],
                "to": leg["destination"]["name"],
                "timestamp": datetime.utcnow().isoformat(),
                "journey_id": entry["_id"]
            })

        # ✅ Save to Redis cache for 5 minutes
        cache_departure(cache_key, entry, ttl=300)

        return {"status": "success", "journey": entry}

    except Exception as e:
        return {"status": "error", "message": str(e)}
