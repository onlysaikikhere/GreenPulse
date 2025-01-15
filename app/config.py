import os

# Example Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '00ecc8357e32a86d3aaf6179df2f5bca')
SOIL_API_KEY = os.environ.get('SOIL_API_KEY', 'your_soil_api_key')
HERE_API_KEY = os.environ.get('HERE_API_KEY', 'aaZehEDfRXG_CJ9YJF4slAfDqFSf9BJSFUbQ3wVoSI8')  # New key for HERE API

# Database Configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///farm_assistant.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False