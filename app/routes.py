#vsr_route_new

from flask import Blueprint, jsonify, request
from app.services.here_maps_service import get_coordinates
from app.models import Location
from app.models import FarmData, db
import requests

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return jsonify({"message": "Welcome to the Farmer's Assistant API!"})

@main.route("/get-location", methods=["POST"])
def get_location():
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude and longitude:
        # Reverse-geocode using HERE API
        api_url = f"https://revgeocode.search.hereapi.com/v1/revgeocode?at={latitude},{longitude}&apiKey=aaZehEDfRXG_CJ9YJF4slAfDqFSf9BJSFUbQ3wVoSI8"
        response = requests.get(api_url)

        if response.status_code != 200:
            return jsonify({"error": "Failed to contact HERE API"}), 500

        location_data = response.json()
        if "items" not in location_data or not location_data["items"]:
            return jsonify({"error": "Location not found"}), 404

        # Return address details
        return jsonify(location_data["items"][0]["address"])

    return jsonify({"error": "Latitude and longitude are required"}), 400


@main.route("/save-location", methods=["POST"])
def save_location():
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    # Fetch soil data using the provided latitude and longitude
    soil_url = "https://rest.isric.org/soilgrids/v2.0/properties/query"
    properties = ["phh2o", "sand", "clay", "silt", "ocd"]
    depths = "0-5cm"  # Query for the topsoil layer
    soil_data = {}

    for prop in properties:
        try:
            response = requests.get(soil_url, params={
                "lon": longitude,
                "lat": latitude,
                "property": prop,
                "depth": depths,
                "value": "mean"
            })
            response.raise_for_status()  # Ensure the request was successful
            soil_response = response.json()

            # Safely extract data
            layers = soil_response.get("properties", {}).get("layers", [])
            if layers:
                depths_data = layers[0].get("depths", [])
                if depths_data:
                    mean_value = depths_data[0].get("values", {}).get("mean")
                    soil_data[prop] = mean_value if mean_value is not None else "N/A"
                else:
                    soil_data[prop] = "N/A"
            else:
                soil_data[prop] = "N/A"
        except Exception as e:
            soil_data[prop] = "N/A"  # Default value in case of errors

    # Adjust the pH value by dividing by 10
    if soil_data.get("phh2o") != "N/A":
        soil_data["phh2o"] = round(soil_data["phh2o"] / 10, 2)

    # Save the location and soil data to the database
    try:
        new_location = Location(
            latitude=latitude,
            longitude=longitude,
            ph=soil_data.get("phh2o") if soil_data.get("phh2o") != "N/A" else None,
            sand=soil_data.get("sand") if soil_data.get("sand") != "N/A" else None,
            clay=soil_data.get("clay") if soil_data.get("clay") != "N/A" else None,
            silt=soil_data.get("silt") if soil_data.get("silt") != "N/A" else None,
            ocd=soil_data.get("ocd") if soil_data.get("ocd") != "N/A" else None
        )
        db.session.add(new_location)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": f"Failed to save location: {str(e)}"}), 500

    return jsonify({"message": "Location and soil data saved successfully", "data": soil_data}), 201
@main.route("/get-soil-data", methods=["POST"])
def get_soil_data():
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if not latitude or not longitude:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    # SoilGrids REST API Base URL
    rest_url = "https://rest.isric.org"
    prop_query_url = f"{rest_url}/soilgrids/v2.0/properties/query"

    # Define soil properties to query
    properties = ["phh2o", "sand", "clay", "silt", "ocd"]
    depth = "0-5cm"  # Query for the top layer of soil

    soil_data = {}

    try:
        for prop in properties:
            params = {
                "lat": latitude,
                "lon": longitude,
                "property": prop,
                "depth": depth,
                "value": "mean"
            }
            response = requests.get(prop_query_url, params=params)
            response.raise_for_status()
            res_data = response.json()

            # Extract the 'mean' value for the property
            mean_value = (
                res_data.get("properties", {})
                .get("layers", [{}])[0]
                .get("depths", [{}])[0]
                .get("values", {})
                .get("mean")
            )
            soil_data[prop] = mean_value if mean_value is not None else "N/A"

        return jsonify(soil_data), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch soil data", "details": str(e)}), 500
