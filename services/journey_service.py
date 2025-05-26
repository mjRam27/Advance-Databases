import requests
from datetime import datetime
from utils.db_mongo import log_trip

def fetch_all_journeys(from_station, to_station):
    url = "https://v5.vbb.transport.rest/journeys"
    params = {
        "from": from_station,
        "to": to_station,
        "results": 3,
        "language": "en",
        "remarks": "true"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        journeys = []
        for journey in data.get("journeys", []):
            for leg in journey.get("legs", []):
                journey_data = {
                    "from": leg["origin"]["name"],
                    "to": leg["destination"]["name"],
                    "departure": datetime.fromisoformat(leg["departure"]).strftime("%H:%M"),
                    "arrival": datetime.fromisoformat(leg["arrival"]).strftime("%H:%M"),
                    "line": leg["line"]["name"],
                    "mode": leg["line"]["productName"],
                    "platform": leg.get("departurePlatform", "N/A"),
                    "delay": leg.get("departureDelay", 0)
                }
                log_trip(journey_data, "all_journeys")
                journeys.append(journey_data)

        return journeys

    except Exception as e:
        print(f"❌ Error in fetch_all_journeys: {e}")
        return {"error": str(e)}
