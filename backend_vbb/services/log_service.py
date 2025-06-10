from pymongo import MongoClient
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["Vbb_transport"]
user_logs_collection = db["user_logs"]

def log_journey(user_id: str, from_station: str, to_station: str, filters: list[str]):
    log = {
        "from_station": from_station,
        "to_station": to_station,
        "filters": filters,
        "timestamp": datetime.now(timezone.utc)
    }

    user_logs_collection.update_one(
        {"user_id": user_id},
        {"$push": {"logs": log}},
        upsert=True
    )
