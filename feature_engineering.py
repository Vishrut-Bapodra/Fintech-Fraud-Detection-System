import pandas as pd
from collections import defaultdict
from utils import z_score, circular_hour_difference, clamp_01
from geospatial import (
    haversine_distance,
     calculate_travel_speed,
     detect_impossible_travel,
     location_risk,
     speed_risk
)

# -------------------------------
# Build User Behavioral Profiles
# -------------------------------

def build_user_profiles(df):
    df["transaction_time"] = pd.to_datetime(df["transaction_time"])

    user_profiles = {}

    for user_id, group in df.groupby("user_id"):

        group = group.sort_values("transaction_time")

        avg_amount = group["transaction_amount"].mean()
        std_amount = group["transaction_amount"].std()

        preferred_hour = group["transaction_time"].dt.hour.mode()[0]

        centroid_lat = group["latitude"].mean()
        centroid_lon = group["longitude"].mean()

        last_row = group.iloc[-1]

        user_profiles[user_id] = {
            "avg_amount": avg_amount,
            "std_amount": std_amount if std_amount > 0 else 1.0,
            "preferred_hour": preferred_hour,
            "centroid_lat": centroid_lat,
            "centroid_lon": centroid_lon,
            "last_transaction_time": last_row["transaction_time"],
            "last_lat": last_row["latitude"],
            "last_lon": last_row["longitude"]
        }

    return user_profiles

# ------------------------------------
# Create Features for New Transaction
# ------------------------------------

def create_transaction_features(user_id, amount, transaction_time, latitude, longitude, user_profiles):
    if user_id not in user_profiles:
        return {
            "new_user": user_id + 1,
            "amount_risk": 0.5,
            "time_risk": 0.5,
            "location_risk": 0.5,
            "speed_risk": 0.0,
            "impossible_travel_flag": 0
        }

    profile = user_profiles[user_id]

    # ---------------------------
    # Amount Deviation
    # ---------------------------
    amount_z = z_score(
        amount,
        profile["avg_amount"],
        profile["std_amount"]
    )

    amount_risk = clamp_01(abs(amount_z) / 5)

    # ---------------------------
    # Time Deviation
    # ---------------------------
    hour_diff = circular_hour_difference(
        transaction_time.hour,
        profile["preferred_hour"]
    )

    time_risk = clamp_01(hour_diff / 12)

    # ---------------------------
    # Location Deviation
    # ---------------------------
    distance_from_centroid = haversine_distance(
        profile["centroid_lat"],
        profile["centroid_lon"],
        latitude,
        longitude
    )
    loc_risk = location_risk(distance_from_centroid)

    # ---------------------------
    # Parse timestamp safely
    # ---------------------------
    time_diff_hours = (
        (transaction_time - profile["last_transaction_time"]).total_seconds() / 3600
    )
    travel_distance = haversine_distance(
        profile["last_lat"],
        profile["last_lon"],
        latitude,
        longitude
    )

    speed = calculate_travel_speed(travel_distance, time_diff_hours)

    speed_anamoly_risk = speed_risk(speed)

    impossible_travel = detect_impossible_travel(speed)

    return {
        "new_user": 0,
        "amount_risk": amount_risk,
        "time_risk": time_risk,
        "location_risk": loc_risk,
        "speed_risk": speed_anamoly_risk,
        "impossible_travel_flag": impossible_travel

    }

