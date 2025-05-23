# services/refresh_service.py
import requests

def refresh_journey(refresh_token: str):
    url = f"https://v5.vbb.transport.rest/journeys/{refresh_token}"
    params = {"stopovers": True, "remarks": True, "language": "en"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()