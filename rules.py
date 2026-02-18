from utils import weighted_risk_score, classify_risk, clamp_01

# ------------------------------------
# Default Weights for Anomaly Signals
# ------------------------------------

DEFAULT_WEIGHTS = {
    "amount_risk": 0.30,
    "time_risk": 0.15,
    "location_risk": 0.25,
    "speed_risk": 0.15,
    "impossible_travel_flag": 0.15
}

# -------------------------------
# Identify Top Risk Drivers
# -------------------------------

def identify_risk_drivers(risk_components, threshold=0.5):

    drivers = []

    if risk_components["amount_risk"] > threshold:
        drivers.append("High amount deviation.")

    if risk_components["time_risk"] > threshold:
        drivers.append("Unusual transaction time.")
    
    if risk_components["location_risk"] > threshold:
        drivers.append("Transaction far from usual location.")
    
    if risk_components["speed_risk"] > threshold:
        drivers.append("High travel speed anomally")
    
    if risk_components["impossible_travel_flag"] == 1:
        drivers.append("Impossible travel detected")

    if not drivers:
        drivers.append("No strong anomally detected")
    
    return drivers

# -------------------------------
# Compute Final Risk Score
# -------------------------------

def compute_risk_score(feature_dict, weights=DEFAULT_WEIGHTS):

    if feature_dict.get("new_user", 0) == 1:
        return{
            "risk_score": 0.5,
            "risk_level": "MEDIUM",
            "drivers": ["New user - insufficient history"]
        }
    
    risk_components = {
        "amount_risk": feature_dict.get("amount_risk", 0),
        "time_risk": feature_dict.get("time_risk",0),
        "location_risk": feature_dict.get("location_risk",0),
        "speed_risk": feature_dict.get("speed_risk",0),
        "impossible_travel_flag": feature_dict.get("impossible_travel_flag",0),
    }

    # Weighted aggregation
    final_score = weighted_risk_score(risk_components, weights)

    # Determine risk levle
    risk_level = classify_risk(final_score)

    #Identify main risk drivers
    drivers = identify_risk_drivers(risk_components)

    return {
        "risk_score": round(clamp_01(final_score), 3),
        "risk_level": risk_level,
        "drivers": drivers
    }
