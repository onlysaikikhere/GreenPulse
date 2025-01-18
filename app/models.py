#vsr_model_new

from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    state = db.Column(db.String(50), nullable=True )
    ph = db.Column(db.Float, nullable=True)  # Ensure nullable=True
    sand = db.Column(db.Float, nullable=True)
    clay = db.Column(db.Float, nullable=True)
    silt = db.Column(db.Float, nullable=True)
    ocd = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Location {self.location_name} ({self.latitude}, {self.longitude})>"