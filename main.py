import pandas as pd
from utils import parse_timestamp
from feature_engineering import build_user_profiles, create_transaction_features
from rules import compute_risk_score


# -------------------------------
# Load Historical Data
# -------------------------------

def load_data(file_path="transaction.csv"):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print("Error loading data:", e)
        exit()


# -------------------------------
# CLI Loop
# -------------------------------

def run_cli(user_profiles):
    print("\n=== Real-Time Behavioral Fraud Detection System ===")

    while True:
        try:
            print("\nEnter New Transaction Details:")
            user_id = int(input("User ID: "))
            amount = float(input("Transaction Amount: "))
            time_str = input("Transaction Time (YYYY-MM-DD HH:MM:SS): ")
            latitude = float(input("Latitude: "))
            longitude = float(input("Longitude: "))

            transaction_time = parse_timestamp(time_str)

            # -------------------------------
            # Feature Engineering
            # -------------------------------
            features = create_transaction_features(
                user_id=user_id,
                amount=amount,
                transaction_time=transaction_time,
                latitude=latitude,
                longitude=longitude,
                user_profiles=user_profiles
            )

            # -------------------------------
            # Risk Scoring
            # -------------------------------
            result = compute_risk_score(features)

            # -------------------------------
            # CLI Loop
            # -------------------------------
            print("\n--- Fraud Risk Assessment ---")
            print(f"Risk Score : {result['risk_score']}")
            print(f"Risk Level : {result['risk_level']}")
            print("Drivers  :")
            for driver in result["drivers"]:
                print(f" -{driver}")
            print("------------------------------")

        except Exception as e:
            print("Error:", e)
        
        cont = input("\nCheck another transaction? (y/n): ")
        if cont.lower() != "y":
            break



# -------------------------------------------------
# Main Execution
# -------------------------------------------------
if __name__ == "__main__":

    # Load historical dataset
    df = load_data("transaction.csv")

    # Build user behavioral baselines
    user_profiles = build_user_profiles(df)

    # Start real-time scoring
    run_cli(user_profiles)