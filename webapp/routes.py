from flask import render_template, Blueprint, request, redirect, url_for, session
from flask_login import login_required, current_user
from flask_login import login_required
from .models import Patient
from .dashboard import generate_patient_data
from . import socketio


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