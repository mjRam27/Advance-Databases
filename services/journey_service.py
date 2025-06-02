import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os
# import json
from utils.db_redis import cache_departure, get_cached_departure

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["Vbb_transport"]
journey_collection = db["journey_logs"]
station_collection = db["station_logs"]

def fetch_journey(from_station: str, to_station: str, products: list[str] = None):
    # ✅ Create a unique cache key
    cache_key = f"{from_station}:{to_station}:{','.join(products or [])}"
    cached = get_cached_departure(cache_key)
    if cached:
        return {"status": "cached", "journey": cached}

    # If not cached, hit the VBB API
    url = "https://v5.vbb.transport.rest/journeys"
    params = {
        "from": from_station,
        "to": to_station,
        "stopovers": True,
        "results": 1,
        "language": "en"
    }
    if products:
        for p in products:
            params.setdefault("products[]", []).append(p)

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("journeys"):
            return {"status": "error", "message": "No journey found"}

        journey = data["journeys"][0]
        leg = journey["legs"][0]

        # Filter stops
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

        # Prepare entry
        entry = {
            "from": leg["origin"]["name"],
            "to": leg["destination"]["name"],
            "line": leg.get("line", {}).get("name"),
            "mode": leg.get("line", {}).get("mode"),
            "platform": leg.get("platform"),
            "delay": leg.get("departureDelay", 0),
            "timestamp": datetime.utcnow().isoformat(),
            "stops": stops
        }

        # Insert into MongoDB
        result = journey_collection.insert_one(entry)
        entry["_id"] = str(result.inserted_id)

        # Optional: update station logs
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

        # ✅ Cache the journey
        cache_departure(cache_key, entry, ttl=300)

        return {"status": "success", "journey": entry}

    except Exception as e:
        return {"status": "error", "message": str(e)}
