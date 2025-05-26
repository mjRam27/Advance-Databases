from services.shared import fetch_departures

def get_re_departures(station_id: str):
    return fetch_departures(station_id, "regional")
