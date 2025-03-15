from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# User model for login authentication
class User(db.Model, UserMixin):
    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Patient model for real-time fluctuating vitals
class Patient(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    blood_group = db.Column(db.String(5), nullable=True)
    date_of_admission = db.Column(db.DateTime(timezone=True), default=func.now())
    medical_history = db.Column(db.String(100), nullable=True)

    # Ranges for dynamically fluctuating vitals
    heart_rate_min = db.Column(db.Integer, nullable=False)
    heart_rate_max = db.Column(db.Integer, nullable=False)
    respiratory_rate_min = db.Column(db.Integer, nullable=False)
    respiratory_rate_max = db.Column(db.Integer, nullable=False)
    body_temperature_min = db.Column(db.Float, nullable=False)
    body_temperature_max = db.Column(db.Float, nullable=False)
    oxygen_saturation_min = db.Column(db.Float, nullable=False)
    oxygen_saturation_max = db.Column(db.Float, nullable=False)
    systolic_bp_min = db.Column(db.Integer, nullable=False)
    systolic_bp_max = db.Column(db.Integer, nullable=False)
    diastolic_bp_min = db.Column(db.Integer, nullable=False)
    diastolic_bp_max = db.Column(db.Integer, nullable=False)

    # Derived Metrics (These may also fluctuate)
    derived_hrv_min = db.Column(db.Float, nullable=True)
    derived_hrv_max = db.Column(db.Float, nullable=True)
    derived_pulse_pressure_min = db.Column(db.Integer, nullable=True)
    derived_pulse_pressure_max = db.Column(db.Integer, nullable=True)
    derived_bmi = db.Column(db.Float, nullable=True)
    derived_map_min = db.Column(db.Float, nullable=True)
    derived_map_max = db.Column(db.Float, nullable=True)

    # # Risk Analysis (Dynamically changing based on ML predictions)
    risk_category = db.Column(db.String(10), nullable=False)
    risk_score_min = db.Column(db.Float, nullable=False)
    risk_score_max = db.Column(db.Float, nullable=False)

    # Risk Factor Probabilities (Fluctuating predictions)
    heart_disease_min = db.Column(db.Float, nullable=False)
    heart_disease_max = db.Column(db.Float, nullable=False)
    hypertension_min = db.Column(db.Float, nullable=False)
    hypertension_max = db.Column(db.Float, nullable=False)
    diabetes_min = db.Column(db.Float, nullable=False)
    diabetes_max = db.Column(db.Float, nullable=False)
    respiratory_issues_min = db.Column(db.Float, nullable=False)
    respiratory_issues_max = db.Column(db.Float, nullable=False)
    obesity_min = db.Column(db.Float, nullable=False)
    obesity_max = db.Column(db.Float, nullable=False)
    stroke_risk_min = db.Column(db.Float, nullable=False)
    stroke_risk_max = db.Column(db.Float, nullable=False)
    survival_probability_min = db.Column(db.Float, nullable=False)
    survival_probability_max = db.Column(db.Float, nullable=False)

    # Timestamp for real-time updates
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
