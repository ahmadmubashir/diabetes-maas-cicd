# backend/model_service.py
import os
import logging
import numpy as np

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Feature order (must match input)
# ------------------------------------------------------------------
FEATURE_NAMES = [
    "age", "hypertension", "heart_disease", "bmi", "hba1c", "blood_glucose",
    "pregnancies", "glucose", "blood_pressure", "skin_thickness", "insulin", "dpf",
    "gender_female", "gender_male", "gender_other", "gender_unknown",
    "current", "ever", "former", "never", "no_info", "not_current", "unknown"
]

def _get_value(obj, key, default=0):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)

def patient_to_vector(patient):
    return np.array([_get_value(patient, name, 0) for name in FEATURE_NAMES], dtype=np.float32)

# ------------------------------------------------------------------
# Dynamic probability using weighted logistic scoring
# (Coefficients derived from typical diabetes risk factors)
# ------------------------------------------------------------------
def dynamic_predict(features):
    # Features index mapping
    idx = {name: i for i, name in enumerate(FEATURE_NAMES)}
    
    # Weighted sum (higher = more risk)
    score = 0.0
    # Continuous risk factors
    score += features[idx["age"]] * 0.02
    score += features[idx["bmi"]] * 0.1
    score += features[idx["hba1c"]] * 0.5
    score += features[idx["blood_glucose"]] * 0.01
    score += features[idx["glucose"]] * 0.008
    score += features[idx["blood_pressure"]] * 0.02
    score += features[idx["insulin"]] * 0.001
    score += features[idx["dpf"]] * 1.2
    # Binary risk factors
    if features[idx["hypertension"]]: score += 2.0
    if features[idx["heart_disease"]]: score += 2.5
    if features[idx["pregnancies"]] > 0: score += features[idx["pregnancies"]] * 0.3
    # Smoking (current worst)
    if features[idx["current"]]: score += 1.5
    if features[idx["former"]]: score += 0.5
    # Gender (male slightly higher)
    if features[idx["gender_male"]]: score += 0.8

    # Convert score to probability using sigmoid-like clamping
    prob = 1 / (1 + np.exp(-(score - 5) / 3))   # score around 5 -> prob 0.5
    prob = np.clip(prob, 0.01, 0.99)
    return float(prob)

def extract_risk_factors(patient):
    factors = []
    bmi = _get_value(patient, "bmi", 0)
    hba1c = _get_value(patient, "hba1c", 0)
    blood_glucose = _get_value(patient, "blood_glucose", 0)
    hypertension = _get_value(patient, "hypertension", 0)
    heart_disease = _get_value(patient, "heart_disease", 0)
    age = _get_value(patient, "age", 0)
    glucose = _get_value(patient, "glucose", 0)
    bp = _get_value(patient, "blood_pressure", 0)

    if bmi >= 30: factors.append("High BMI")
    if hba1c >= 6.5: factors.append("Elevated HbA1c")
    if blood_glucose >= 140: factors.append("Elevated Blood Glucose")
    if glucose >= 140: factors.append("High Glucose")
    if hypertension == 1: factors.append("Hypertension")
    if heart_disease == 1: factors.append("Heart Disease")
    if age >= 60: factors.append("Older Age")
    if bp >= 140: factors.append("High Blood Pressure")
    if _get_value(patient, "current") == 1: factors.append("Current Smoker")
    return factors

def predict_diabetes(patient):
    features = patient_to_vector(patient)
    probability = dynamic_predict(features)
    
    prediction = "Diabetic" if probability >= 0.5 else "Non-Diabetic"
    if probability >= 0.80: risk_level = "Very High Risk"
    elif probability >= 0.60: risk_level = "High Risk"
    elif probability >= 0.40: risk_level = "Moderate Risk"
    else: risk_level = "Low Risk"
    
    confidence = max(probability, 1 - probability)
    risk_factors = extract_risk_factors(patient)

    return {
        "prediction": prediction,
        "probability": probability,
        "confidence": confidence,
        "risk_level": risk_level,
        "risk_factors": risk_factors
    }