import math
from utils import safe_divide, clamp_01

# ---------------------------
# Haversine Distance
# ---------------------------

def haversine_distance(lat1, lon1, lat2, lon2):
    
    R = 6371
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)


    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon2_rad

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1_rad) * 
         math.cos(lat2_rad) * 
         math.sin(dlon / 2) ** 2)
    
    c = 2* math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# ---------------------------
# Travel Speed (km/h)
# ---------------------------

def calculate_travel_speed(distance_km, time_diff_hours):
    return safe_divide(distance_km, time_diff_hours, default=0.0)

# ----------------------------
# Impossible Travel Detection
# ----------------------------

def detect_impossible_travel(speed_kmh, threshold=900):
    return 1 if speed_kmh > threshold else 0

# ---------------------------
# Location Deviation Risk
# ---------------------------

def location_risk(distance_from_centroid, max_distance=500):
    return clamp_01(distance_from_centroid / max_distance)

# ---------------------------
# Travel Speed Risk Scaling
# ---------------------------

def speed_risk(speed_kmh, max_speed=1200):
    return clamp_01(speed_kmh / max_speed)