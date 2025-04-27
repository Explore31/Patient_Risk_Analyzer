from flask import render_template, Blueprint, request, redirect, url_for, session, jsonify
from flask_login import login_required, current_user
from flask_login import login_required
from .models import Patient
from .dashboard import generate_patient_data
from . import socketio
from .import db
from datetime import datetime


routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return redirect(url_for('auth.login'))

@routes.route('/patient_id', methods=['GET', 'POST'])
@login_required
def patient_id():
    patients = Patient.query.all()

    if request.method == 'POST':
        patient_id = request.form.get('patient_id', '').strip()
        patient_name = request.form.get('patient_name', '').strip()

        patient_by_id = None
        patient_by_name = None

        if patient_id:
            patient_by_id = Patient.query.filter_by(id=patient_id).first()
        if patient_name:
            patient_by_name = Patient.query.filter_by(name=patient_name).first()

        # Case 1: Neither Patient ID nor Name is found
        if not patient_by_id and not patient_by_name:
            return render_template('select.html', patients=patients, error = "PID not found!")
        
        # Case 2: Only Patient ID was entered and found
        if patient_by_id and not patient_name:
            session['patient_id'] = patient_by_id.id
            return redirect(url_for('routes.index'))
        
        # Case 3: Only Patient Name was entered and found
        if patient_by_name and not patient_id:
            session['patient_id'] = patient_by_name.id
            return redirect(url_for('routes.index'))
        
        # Case 4: Both Patient ID and Name were entered and checked for match.
        if patient_by_id and patient_by_name:
            # If both ID and Name match, proceed to dashboard
            if patient_by_id.id == patient_by_name.id:
                session['patient_id'] = patient_by_id.id
                return redirect(url_for('routes.index'))
            # If both ID and Name do not match, return error
            else:
                # return "PID & Name mismatch", 400
                return render_template('select.html', patients=patients, error = "PID and name mismatch")

    return render_template('select.html', patients=patients)

@routes.route('/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        blood_group = request.form['blood_group']
        medical_history = request.form.get('medical_history', '')

        # Generate new Patient ID
        prefix = f"SC2025{'M' if gender == 'Male' else 'F'}"
        existing = Patient.query.filter(Patient.id.like(f"{prefix}%")).count()
        patient_id = f"{prefix}{existing + 101}"

        # Create new Patient instance with required defaults and placeholder ranges
        new_patient = Patient(
            id=patient_id,
            name=name,
            age=age,
            gender=gender,
            weight=weight,
            height=height,
            blood_group=blood_group,
            date_of_admission=datetime.now(),
            medical_history=medical_history,
            heart_rate_min=60, heart_rate_max=100,
            respiratory_rate_min=12, respiratory_rate_max=20,
            body_temperature_min=36.5, body_temperature_max=37.5,
            oxygen_saturation_min=95.0, oxygen_saturation_max=99.0,
            systolic_bp_min=110, systolic_bp_max=130,
            diastolic_bp_min=70, diastolic_bp_max=90,
            derived_hrv_min=0.1, derived_hrv_max=0.15,
            derived_pulse_pressure_min=40, derived_pulse_pressure_max=50,
            derived_bmi=round(weight / (height ** 2), 1),
            derived_map_min=85.0, derived_map_max=100.0,
            risk_category="Low Risk",
            risk_score_min=5.0, risk_score_max=10.0,
            heart_disease_min=0.1, heart_disease_max=0.2,
            hypertension_min=0.1, hypertension_max=0.2,
            diabetes_min=0.05, diabetes_max=0.1,
            respiratory_issues_min=0.05, respiratory_issues_max=0.1,
            obesity_min=0.15, obesity_max=0.25,
            stroke_risk_min=0.05, stroke_risk_max=0.1,
            survival_probability_min=90.0, survival_probability_max=100.0
        )

        db.session.add(new_patient)
        db.session.commit()

        # If it's an AJAX (fetch) call, return JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(success=True)

        return redirect(url_for('routes.patient_id'))

    return render_template('add.html')


@routes.route('/dashboard')
@login_required
def index():
    patient_id = session.get('patient_id')
    patient = Patient.query.get(patient_id)
    if not patient_id:
        return redirect(url_for('routes.patient_id'))
    return render_template('dashboard.html', patient_id=patient_id, patient=patient, user = current_user.id)

# WebSocket event for real-time data streaming
@socketio.on('request_data')
def stream_data():
    patient_id = session.get('patient_id')
    patient = Patient.query.get(patient_id)
    if not patient:
        return
    while True:
        patient_data = generate_patient_data(patient)
        socketio.emit('update_vitals', patient_data)
        socketio.sleep(2)