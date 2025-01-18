#vsr_route_new

from flask import Blueprint, jsonify, request
from app.services.here_maps_service import get_coordinates
from app.models import Location
from app.models import  db
import requests
import json
import os

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
        api_url = f"https://revgeocode.search.hereapi.com/v1/revgeocode"
        params = {
            "at": f"{latitude},{longitude}",
            "apiKey": "aaZehEDfRXG_CJ9YJF4slAfDqFSf9BJSFUbQ3wVoSI8",
            "lang": "en-US",
            "limit": 1
        }
        
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()

            location_data = response.json()
            if "items" not in location_data or not location_data["items"]:
                return jsonify({"error": "Location not found"}), 404

            # Extract state name with fallbacks
            address = location_data["items"][0]["address"]
            state = (
                address.get("state") or 
                address.get("stateCode") or 
                address.get("county") or 
                address.get("administrativeArea") or
                "Unknown State"
            )

            # For debugging
            print("Full address response:", address)

            return jsonify({
                "latitude": latitude,
                "longitude": longitude,
                "state": state,
                "full_address": address  # Optional: include full address for debugging
            })

        except requests.exceptions.RequestException as e:
            print(f"API Error: {str(e)}")
            return jsonify({"error": f"Failed to contact HERE API: {str(e)}"}), 500

    return jsonify({"error": "Latitude and longitude are required"}), 400


@main.route("/save-location", methods=["POST"])
def save_location():
    try:
        # Print the raw request data
        print("Raw request data:", request.get_data())
        
        data = request.get_json()
        print("Parsed JSON data:", data)
        
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        state = data.get("state")
        soil_data = data.get("soil_data", {})

        print(f"""
Debug Info:
-----------
Latitude: {latitude}
Longitude: {longitude}
State: {state}
Soil Data: {soil_data}
        """)

        if not all([latitude, longitude]):
            print("Validation failed: Missing latitude or longitude")
            return jsonify({"error": "Latitude and longitude are required"}), 400

        # Save to the database
        try:
            new_location = Location(
                latitude=latitude,
                longitude=longitude,
                state=state,
                ph=soil_data.get("phh2o"),
                sand=soil_data.get("sand"),
                clay=soil_data.get("clay"),
                silt=soil_data.get("silt"),
                ocd=soil_data.get("ocd")
            )
            print("Created Location object:", vars(new_location))
            
            db.session.add(new_location)
            db.session.commit()
            print("Database save successful")
            
        except Exception as db_error:
            print(f"Database error: {str(db_error)}")
            db.session.rollback()
            raise

        # File operations
        recents_file = "recents.json"
        print(f"Working with recents file: {recents_file}")
        
        try:
            # Create recents.json if it doesn't exist
            if not os.path.exists(recents_file):
                print("Creating new recents.json file")
                with open(recents_file, "w") as file:
                    json.dump({}, file)

            # Load existing data
            try:
                with open(recents_file, "r") as file:
                    recents_data = json.load(file)
                    print("Loaded existing data:", recents_data)
            except json.JSONDecodeError as json_error:
                print(f"JSON decode error: {str(json_error)}")
                recents_data = {}

            # Ensure state exists in the data
            if state not in recents_data:
                print(f"Creating new state entry for: {state}")
                recents_data[state] = {}

            # Create location key
            location_key = f"{latitude:.6f}-{longitude:.6f}"
            print(f"Using location key: {location_key}")
            
            # Update soil data
            recents_data[state][location_key] = {
                "phh2o": soil_data.get("phh2o"),
                "sand": soil_data.get("sand"),
                "clay": soil_data.get("clay"),
                "silt": soil_data.get("silt"),
                "ocd": soil_data.get("ocd")
            }
            print("Updated data structure:", recents_data)

            # Write the file
            try:
                with open(recents_file, "w") as file:
                    json.dump(recents_data, file, indent=4)
                print("Successfully wrote to recents.json")
                
            except Exception as write_error:
                print(f"File write error: {str(write_error)}")
                raise

            return jsonify({
                "message": "Location and soil data saved successfully",
                "state": state,
                "location_key": location_key,
                "debug": "Check server console for detailed logs"
            }), 201

        except Exception as file_error:
            print(f"File operation error: {str(file_error)}")
            raise

    except Exception as e:
        print(f"Top level error: {str(e)}")
        print(f"Error type: {type(e)}")
        return jsonify({
            "error": f"Failed to save location: {str(e)}",
            "error_type": str(type(e)),
            "debug": "Check server console for detailed logs"
        }), 500
    

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
