import requests
from utils.db_mongo import log_trip
from bson.errors import InvalidDocument  # catch specific MongoDB errors

# Define mode groups, normalize everything to lowercase
MODE_GROUPS = {
    "bus": ["bus"],
    "tram": ["tram"],
    "subway": ["subway"],
    "suburban": ["suburban"],
    "regional": ["regional"],
    "express": ["express", "ice", "fex", "flx"]
}

def fetch_departures(station_id: str, transport_type: str, duration: int = 120):
    url = f"https://v5.vbb.transport.rest/stops/{station_id}/departures"
    params = {
        "duration": duration,
        "language": "en",
        "remarks": "true"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        accepted_products = MODE_GROUPS.get(transport_type.lower(), [])

        for trip in data:
            line = trip.get("line", {})
            mode = line.get("product", "").lower()

            # Debug print: you can remove these later
            print(f"✅ Found line: {line.get('name')} with product: {mode}")

            if mode not in accepted_products:
                continue

            result = {
                "from": trip.get("stop", {}).get("name"),
                "to": trip.get("direction"),
                "departure": trip.get("when"),
                "plannedDeparture": trip.get("plannedWhen"),
                "delay": trip.get("delay"),
                "platform": trip.get("platform"),
                "line": line.get("name"),
                "mode": mode,
            }

            # Insert into MongoDB with safety
            try:
                log_trip(result, f"{transport_type.lower()}_logs")
                print(f"✅ Inserted into MongoDB for {transport_type}")
            except InvalidDocument as mongo_err:
                print(f"❌ Invalid MongoDB Document: {mongo_err}")
            except Exception as err:
                print(f"❌ General MongoDB Insert Error: {err}")

            results.append(result)

        return results if results else [{"note": f"No {transport_type.upper()} departures found."}]

    except requests.exceptions.RequestException as net_err:
        print(f"❌ Network/API error: {net_err}")
        return {"error": "API unreachable or bad request."}

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return {"error": str(e)}
