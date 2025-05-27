# services/journey_service.py

import requests

def fetch_journey(from_station: str, to_station: str):
    url = "https://v5.vbb.transport.rest/journeys"
    params = {
        "from": from_station,
        "to": to_station,
        "stopovers": True,
        "results": 1,
        "language": "en"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "status": "success",
            "journey": data["journeys"][0] if data.get("journeys") else "No journey found"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
