import requests
from urllib.parse import quote_plus

def get_station_id(station_name: str) -> str:
    try:
        # Make sure the station name is URL-safe (e.g. "Berlin Hbf" → "Berlin+Hbf")
        encoded_name = quote_plus(station_name)
        url = f"https://v5.vbb.transport.rest/locations?query={encoded_name}"

        response = requests.get(url)

        # Check if the response is OK
        if response.status_code != 200:
            raise RuntimeError(f"API returned {response.status_code}: {response.text}")

        data = response.json()

        if not data:
            raise RuntimeError("No station found.")

        return data[0]["id"]

    except Exception as e:
        raise RuntimeError(f"Error fetching station ID: {e}")
