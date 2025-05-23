# bus_service.py:
from services.shared import fetch_mode_data
def fetch_bus_data(from_station, to_station):
    return fetch_mode_data(from_station, to_station, "bus")