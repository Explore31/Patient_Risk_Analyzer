from webapp import db
from webapp.models import User, Patient
from werkzeug.security import generate_password_hash
from datetime import datetime

def populate_database():
    with db.session.begin():
        # Check if users and patients already exist
        if not User.query.first():
            test_user = User(id="SCUSR01", username="test@mail.com", name="Dolittle", password=generate_password_hash("test123"))
            db.session.add(test_user)

        if not Patient.query.first():
            patients = [
                Patient(id="SC2025TST1", name="John Doe", age=45, gender="Male", weight=80, height=1.75, blood_group="O+",
                        date_of_admission=datetime(2025, 3, 10, 14, 30), #medical_history="None",
                        heart_rate_min=68, heart_rate_max=75, respiratory_rate_min=14, respiratory_rate_max=18,
                        body_temperature_min=36.5, body_temperature_max=37.2, oxygen_saturation_min=97.0, oxygen_saturation_max=99.0,
                        systolic_bp_min=115, systolic_bp_max=125, diastolic_bp_min=75, diastolic_bp_max=85,
                        derived_hrv_min=0.10, derived_hrv_max=0.14, derived_pulse_pressure_min=35, derived_pulse_pressure_max=45,
                        derived_bmi=26.1, derived_map_min=90.0, derived_map_max=95.0,
                        risk_category="Low Risk", risk_score_min=10.0, risk_score_max=15.0,
                        heart_disease_min=0.05, heart_disease_max=0.15, hypertension_min=0.1, hypertension_max=0.2,
                        diabetes_min=0.02, diabetes_max=0.08, respiratory_issues_min=0.05, respiratory_issues_max=0.12,
                        obesity_min=0.12, obesity_max=0.18, stroke_risk_min=0.03, stroke_risk_max=0.07, 
                        survival_probability_min=93.0, survival_probability_max=98.0),

                Patient(id="SC2025TST2", name="Jane Smith", age=60, gender="Female", weight=75, height=1.65, blood_group="A+",
                        date_of_admission=datetime(2025, 3, 10, 14, 30), #medical_history="None",
                        heart_rate_min=76, heart_rate_max=85, respiratory_rate_min=16, respiratory_rate_max=20,
                        body_temperature_min=36.8, body_temperature_max=37.5, oxygen_saturation_min=94.0, oxygen_saturation_max=97.5,
                        systolic_bp_min=125, systolic_bp_max=135, diastolic_bp_min=80, diastolic_bp_max=90,
                        derived_hrv_min=0.07, derived_hrv_max=0.11, derived_pulse_pressure_min=40, derived_pulse_pressure_max=50,
                        derived_bmi=27.6, derived_map_min=95.0, derived_map_max=105.0,
                        risk_category="High Risk", risk_score_min=75.0, risk_score_max=85.0,
                        heart_disease_min=0.55, heart_disease_max=0.65, hypertension_min=0.7, hypertension_max=0.85,
                        diabetes_min=0.35, diabetes_max=0.45, respiratory_issues_min=0.25, respiratory_issues_max=0.35,
                        obesity_min=0.65, obesity_max=0.75, stroke_risk_min=0.35, stroke_risk_max=0.45, 
                        survival_probability_min=55.0, survival_probability_max=65.0),
            ]

            db.session.add_all(patients)

        db.session.commit()
        print("Database populated successfully!")

