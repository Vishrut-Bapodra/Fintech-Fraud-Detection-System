from datetime import datetime

# ---------------------------
# Safe Division
# ---------------------------

def safe_divide(a, b, default=0.0):
    if b == 0:
        return default
    return a/b

# ----------------------------
# Clamp value between 0 and 1
# ----------------------------

def clamp_01(value):
    return max(0.0, min(1.0, value))

# ------------------------------------------------
# Normalize value between 0 and 1 using max scale
# ------------------------------------------------

def normalize(value, max_value):
    if max_value == 0:
        return 0.0
    
    return clamp_01(value / max_value)

# ---------------------------
# Z-Score Calculation
# ---------------------------

def z_score(value, mean, std):
    std = std if std > 0 else 1e-6
    return (value - mean) / std

# ---------------------------
# Parse timestamp safely
# ---------------------------

def parse_timestamp(time_str):

    try:
        return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        raise ValueError("Invalid timestamp format. Use YYYY-MM-DD HH:MM:SS")
    
# -----------------------------------
# Compute hour difference circularly 
# -----------------------------------

def circular_hour_difference(hour1, hour2):
    diff = abs(hour1 - hour2)
    return min(diff, 24 - diff)

# ---------------------------
# Weighted Risk Aggregation
# ---------------------------

def weighted_risk_score(risk_components, weights):
    
    total_score = 0.0
    total_weight = 0.0

    for key in risk_components:
        weight = weights.get(key, 0)
        total_score += risk_components[key] * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0
    
    return clamp_01(total_score / total_weight)

# ---------------------------
# Risk Level Classification
# ---------------------------

def classify_risk(score):
    if score < 0.3:
        return "LOW"
    elif score < 0.6:
        return "MEDIUM"
    elif score < 0.8:
        return "HIGH"
    else:
        return "CRITICAL"