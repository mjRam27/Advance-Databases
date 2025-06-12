from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from utils.db_mongo import user_collection

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["Vbb_transport"]
user_logs_collection = db["user_logs"]

router = APIRouter()

# 📦 Journey Log Schema
class JourneyLog(BaseModel):
    user_id: str
    from_station: str
    to_station: str
    filters: list[str]

# 🔁 Log a journey
@router.post("/log")
def log_journey_endpoint(log: JourneyLog):
    log_data = {
        "from_station": log.from_station,
        "to_station": log.to_station,
        "filters": log.filters,
        "timestamp": datetime.now(timezone.utc)
    }

    user_logs_collection.update_one(
        {"user_id": log.user_id},
        {"$push": {"logs": log_data}},
        upsert=True
    )

    return {"message": "Journey logged successfully"}

# 📄 Get recent 5 journeys
@router.get("/journey/recent")
def recent_journeys(user_id: str):
    record = user_logs_collection.find_one({"user_id": user_id})
    if not record or "logs" not in record:
        return {"recent": []}

    recent = sorted(record["logs"], key=lambda x: x["timestamp"], reverse=True)[:5]

    return {
        "recent": [
            {"from_id": log["from_station"], "to_id": log["to_station"]}
            for log in recent
        ]
    }
