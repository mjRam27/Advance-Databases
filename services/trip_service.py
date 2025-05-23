import requests
# from utils.resolve import get_station_id

def fetch_trip_by_id(trip_id: str):
    url = f"https://v5.vbb.transport.rest/trips/{trip_id}"
    params = {"stopovers": True, "remarks": True, "language": "en"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def fetch_journey_and_trip(from_name: str, to_name: str):
    from_id = get_station_id(from_name)
    to_id = get_station_id(to_name)

    url = "https://v5.vbb.transport.rest/journeys"
    params = {
        "from": "900000003201",
        "to": "900000320003",
        "results": 1,
        "language": "en",
        "remarks": "true"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Get trip ID from first journey leg
    try:
        trip_id = data["journeys"][0]["legs"][0]["tripId"]
        return trip_id
    except (IndexError, KeyError):
        raise ValueError("Trip ID not found in journey.")
