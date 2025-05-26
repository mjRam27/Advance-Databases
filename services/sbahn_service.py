from services.shared import fetch_departures

def get_sbahn_departures(station_id: str):
    return fetch_departures(station_id, "suburban")
