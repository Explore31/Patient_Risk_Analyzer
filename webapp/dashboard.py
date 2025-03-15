from flask import Blueprint, session
from .models import Patient
from . import socketio
from ml_models import risk_model, risk_score_model, risk_factor_model, survival_model
import pandas as pd
import random


dashboard = Blueprint("dashboard", __name__)

MEDICAL_CONDITIONS = ["Heart Disease", "Hypertension", "Diabetes", "Respiratory Issues", "Obesity", "Stroke Risk"]

# Function to generate real-time fluctuating vitals
def generate_patient_data(patient):
    return {
        "Heart Rate": random.randint(patient.heart_rate_min, patient.heart_rate_max),
        "Respiratory Rate": random.randint(patient.respiratory_rate_min, patient.respiratory_rate_max),
        "Body Temperature": round(random.uniform(patient.body_temperature_min, patient.body_temperature_max), 1),
        "Oxygen Saturation": round(random.uniform(patient.oxygen_saturation_min, patient.oxygen_saturation_max), 1),
        "Systolic Blood Pressure": random.randint(patient.systolic_bp_min, patient.systolic_bp_max),
        "Diastolic Blood Pressure": random.randint(patient.diastolic_bp_min, patient.diastolic_bp_max),
        "Name": patient.name,
        "Age": patient.age,
        "Gender": patient.gender,
        "Weight (kg)": patient.weight,
        "Height (m)": patient.height,
        "Blood Group": patient.blood_group,
        "Date of Admission": patient.date_of_admission.strftime("%Y-%m-%d"),
        "Derived_HRV": round(random.uniform(patient.derived_hrv_min, patient.derived_hrv_max), 1),
        "Derived_Pulse_Pressure": random.randint(patient.derived_pulse_pressure_min, patient.derived_pulse_pressure_max),
        "Derived_BMI": round(patient.weight / (patient.height ** 2), 1),
        "Derived_MAP": round(random.uniform(patient.derived_map_min, patient.derived_map_max), 1),
        "Medical History": patient.medical_history,
        "Risk Category": patient.risk_category,
        "Risk Score": round(random.uniform(patient.risk_score_min, patient.risk_score_max), 2),
        "Heart Disease Risk": round(random.uniform(patient.heart_disease_min, patient.heart_disease_max), 2),
        "Hypertension Risk": round(random.uniform(patient.hypertension_min, patient.hypertension_max), 2),
        "Diabetes Risk": round(random.uniform(patient.diabetes_min, patient.diabetes_max), 2),
        "Respiratory Issues Risk": round(random.uniform(patient.respiratory_issues_min, patient.respiratory_issues_max), 2),
        "Obesity Risk": round(random.uniform(patient.obesity_min, patient.obesity_max), 2),
        "Stroke Risk": round(random.uniform(patient.stroke_risk_min, patient.stroke_risk_max), 2),
        "Survival Probability": round(random.uniform(patient.survival_probability_min, patient.survival_probability_max), 2),
    }

def predict_risk_category(patient_data):
    """
    Predicts the risk category (High Risk or Low Risk) for a given patient.
    
    Parameters:
        patient_data (dict): Patient features in dictionary format.
    
    Returns:
        str: "High Risk" or "Low Risk"
    """
    # Convert Gender to Numeric (Male → 0, Female → 1)
    patient_data["Gender"] = 0 if patient_data["Gender"] == "Male" else 1

    # One-Hot Encode Medical History
    medical_history = patient_data.get("Medical History", "")  # Default to empty string if missing
    if medical_history is None:
        medical_history = ""
    for condition in MEDICAL_CONDITIONS:
        patient_data[condition] = 1 if condition in medical_history else 0

    # Define expected feature order (must match training data)
    feature_order = [
        "Heart Rate", "Respiratory Rate", "Body Temperature", "Oxygen Saturation",
        "Systolic Blood Pressure", "Diastolic Blood Pressure", "Age", "Gender",
        "Weight (kg)", "Height (m)", "Derived_HRV", "Derived_Pulse_Pressure",
        "Derived_BMI", "Derived_MAP", "Heart Disease", "Diabetes", "Hypertension",
        "Respiratory Issues", "Obesity", "Stroke Risk"
    ]

    # Convert patient data to Pandas DataFrame
    input_df = pd.DataFrame([patient_data], columns=feature_order)

    # Make prediction
    prediction = risk_model.predict(input_df)[0]

    return "High Risk" if prediction == 1 else "Low Risk"

def predict_risk_score(patient_data):
    """
    Predicts the risk score (%) for a given patient.
    
    Parameters:
        patient_data (dict): Patient features in a dictionary format (same as dataset format).
    
    Returns:
        float: Predicted Risk Score (%).
    """
    # Convert Gender to Numeric
    patient_data["Gender"] = 0 if patient_data["Gender"] == "Male" else 1

    # One-Hot Encode Medical History
    medical_history = patient_data.get("Medical History", "")  # Default to empty string if missing
    if medical_history is None:
        medical_history = ""
    for condition in MEDICAL_CONDITIONS:
        patient_data[condition] = 1 if condition in medical_history else 0

    # Define the expected feature order
    feature_order = [
        "Heart Rate", "Respiratory Rate", "Body Temperature", "Oxygen Saturation",
        "Systolic Blood Pressure", "Diastolic Blood Pressure", "Age", "Gender",
        "Weight (kg)", "Height (m)", "Derived_HRV", "Derived_Pulse_Pressure",
        "Derived_BMI", "Derived_MAP", "Heart Disease", "Diabetes", "Hypertension",
        "Respiratory Issues", "Obesity", "Stroke Risk"
    ]

    # Convert patient data to Pandas DataFrame
    input_df = pd.DataFrame([patient_data], columns=feature_order)

    # Predict Risk Score
    risk_score = risk_score_model.predict(input_df)[0]

    return round(risk_score,2)  # Return rounded risk score

# Function
def predict_risk_factors(patient_data):
    """Predicts the risk factor probabilities for a given patient."""
    
    # Convert Gender to numeric
    patient_data["Gender"] = 0 if patient_data["Gender"] == "Male" else 1

    # Ensure feature names match exactly what the model was trained on
    expected_features = [
        "Heart Rate", "Respiratory Rate", "Body Temperature", "Oxygen Saturation",
        "Systolic Blood Pressure", "Diastolic Blood Pressure", "Age", "Gender",
        "Weight (kg)", "Height (m)", "Derived_HRV", "Derived_Pulse_Pressure",
        "Derived_BMI", "Derived_MAP"
    ]
    
    # Create DataFrame and reorder columns
    input_df = pd.DataFrame([patient_data])
    input_df = input_df.reindex(columns=expected_features, fill_value=0)  # Fill missing values with 0

    # Predict risk factor probabilities
    predictions = risk_factor_model.predict(input_df)[0]

    # Format results
    risk_factors = {
        "Heart Disease (%)": round(predictions[0] * 100, 2),
        "Hypertension (%)": round(predictions[1] * 100, 2),
        "Diabetes (%)": round(predictions[2] * 100, 2),
        "Respiratory Issues (%)": round(predictions[3] * 100, 2),
        "Obesity (%)": round(predictions[4] * 100, 2),
        "Stroke Risk (%)": round(predictions[5] * 100, 2)
    }

    return risk_factors

def predict_survival_probability(patient_data):
    """Predicts the survival probability for a given patient."""
    
    patient_data["Gender"] = 0 if patient_data["Gender"] == "Male" else 1

    # Ensure feature names match exactly what the model was trained on
    expected_features = [
        "Heart Rate", "Respiratory Rate", "Body Temperature", "Oxygen Saturation",
        "Systolic Blood Pressure", "Diastolic Blood Pressure", "Age", "Gender",
        "Weight (kg)", "Height (m)", "Derived_HRV", "Derived_Pulse_Pressure",
        "Derived_BMI", "Derived_MAP"
    ]
    
    # Create DataFrame and reorder columns
    input_df = pd.DataFrame([patient_data])
    input_df = input_df.reindex(columns=expected_features, fill_value=0)  # Fill missing values with 0

    # Predict survival probability
    prediction = survival_model.predict(input_df)[0]

    # Format result
    survival_percentage = round(prediction, 2)

    return survival_percentage

#function to generate pipeline predictions using generated patient data using the models
@socketio.on("request_live_data")
def generate_pipeline_predictions():
    patient_id = session.get("patient_id")
    if not patient_id:
        print("❌ No patient ID found in session!")
        return
    
    patient = Patient.query.get(patient_id)
    if not patient:
        print("❌ Patient not found in database!")
        return

    def emit_data():
        while True:
            patient_data = generate_patient_data(patient)
            risk_category = predict_risk_category(patient_data)
            risk_score = predict_risk_score(patient_data)
            risk_factors = predict_risk_factors(patient_data)
            survival_probability = predict_survival_probability(patient_data)

            socketio.emit("update_live_data", {
                "patient_data": patient_data,
                "risk_category": risk_category,
                "risk_score": risk_score,
                "risk_factors": risk_factors,
                "survival_probability": survival_probability
            })
            socketio.sleep(5)

    socketio.start_background_task(target=emit_data)



