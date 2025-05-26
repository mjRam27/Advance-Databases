from services.shared import fetch_departures

def get_ubahn_departures(station_id: str):
    return fetch_departures(station_id, "subway")
