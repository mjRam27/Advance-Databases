# utils/db_mongo.py
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["vbb_db"]
def log_trip(data, collection):
    db[collection].insert_one(data)