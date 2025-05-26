from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
db = client["vbb_db"]

def log_trip(trip_data: dict, collection_name: str):
    collection = db[collection_name]
    inserted = collection.insert_one(trip_data)
    return str(inserted.inserted_id)  # <-- Convert ObjectId to string
