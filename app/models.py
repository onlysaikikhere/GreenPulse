#vsr_model_new

from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FarmData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    soil_type = db.Column(db.String(100), nullable=True)
    crop_preferences = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farm_data.id'), nullable=False)
    weather_summary = db.Column(db.String(500), nullable=False)
    final_suggestion = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=True)  # Ensure nullable=True
    sand = db.Column(db.Float, nullable=True)
    clay = db.Column(db.Float, nullable=True)
    silt = db.Column(db.Float, nullable=True)
    ocd = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Location {self.location_name} ({self.latitude}, {self.longitude})>"