import requests

def fetch_departures(station_id: str, duration: int = 60):
    url = f"https://v5.vbb.transport.rest/stops/{station_id}/departures"
    params = {
        "duration": duration,
        "language": "en"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    raw_departures = response.json()

    departures = []

    for dep in raw_departures:
        departures.append({
            "tripId": dep.get("tripId"),
            "line": dep.get("line", {}).get("name", "N/A"),
            "direction": dep.get("direction", "Unknown"),
            "when": dep.get("when"),
            "plannedWhen": dep.get("plannedWhen"),
            "delay": dep.get("delay", 0),  # in seconds
            "platform": dep.get("platform", "N/A"),
            "mode": dep.get("line", {}).get("mode", "N/A")  # e.g. bus, subway
        })

    return departures
