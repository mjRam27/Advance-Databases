from urllib.parse import quote
import requests

def encode_station_name(name: str) -> str:
    """URL-encodes a station name to be used in a query string."""
    return quote(name)

def get_station_id(station_name: str) -> str:
    """Fetches station ID using VBB's /locations endpoint."""
    try:
        url = f"https://v5.vbb.transport.rest/locations?query={quote(station_name)}"
        response = requests.get(url)
        data = response.json()

        if isinstance(data, list) and data and "id" in data[0]:
            return data[0]["id"]
        raise ValueError("Station ID not found.")

    except Exception as e:
        raise RuntimeError(f"Error fetching station ID: {e}")
