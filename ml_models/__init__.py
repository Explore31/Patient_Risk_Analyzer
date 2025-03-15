import pickle
import os

# Define the path to the models directory
MODEL_DIR = os.path.dirname(__file__)

# Load ML models
with open(os.path.join(MODEL_DIR, "riskPredictor.pkl"), "rb") as file:
    risk_model = pickle.load(file)

with open(os.path.join(MODEL_DIR, "riskScore_regr.pkl"), "rb") as file:
    risk_score_model = pickle.load(file)

with open(os.path.join(MODEL_DIR, "riskfactor_prob.pkl"), "rb") as file:
    risk_factor_model = pickle.load(file)

with open(os.path.join(MODEL_DIR, "survivalProbability.pkl"), "rb") as file:
    survival_model = pickle.load(file)
