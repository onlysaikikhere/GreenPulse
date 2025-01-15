import requests
from app.config import HERE_API_KEY

BASE_URL = "https://geocode.search.hereapi.com/v1/geocode"

def get_coordinates(address):
    """
    Get latitude and longitude for a given address using the HERE API.
    :param address: String, farm location address.
    :return: Dictionary with latitude and longitude or an error message.
    """
    try:
        params = {
            "q": address,
            "apiKey": HERE_API_KEY,
        }
        response = requests.get(BASE_URL, params=params)
        response_data = response.json()

        if response.status_code == 200 and "items" in response_data and len(response_data["items"]) > 0:
            location = response_data["items"][0]["position"]
            return {"latitude": location["lat"], "longitude": location["lng"]}
        else:
            return {"error": "Address not found"}
    except Exception as e:
        return {"error": str(e)}
