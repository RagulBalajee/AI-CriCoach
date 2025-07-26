# main.py

from scripts.feature_engineering import load_data, engineer_features
from scripts.predictor import train_model, load_model
from scripts.strategy_engine import suggest_bowler, suggest_field

def run_training():
    try:
        df = load_data("data/deliveries.csv")
        print("[INFO] Data loaded successfully.")
        df_features = engineer_features(df)
        train_model(df_features)
        print("[SUCCESS] Model trained and saved.")
    except FileNotFoundError:
        print("[ERROR] deliveries.csv not found in data/. Please download and place it there.")
    except Exception as e:
        print(f"[ERROR] An error occurred during training: {e}")

def run_live_demo():
    try:
        model = load_model()
        print("[INFO] Model loaded.")

        # Simulated match state (in a real system, fetch this from live data)
        live_input = {
            "overs": 15,
            "score": 120,
            "wickets": 4,
            "run_rate": 8.0,
            "wicket_rate": 0.27,
            "target_remaining": 60,
            "pitch": "dry",
            "required_rate": 9.5
        }

        # Predict win probability
        features = [[
            live_input["overs"],
            live_input["score"],
            live_input["wickets"],
            live_input["run_rate"],
            live_input["wicket_rate"],
            live_input["target_remaining"]
        ]]
        win_prob = model.predict_proba(features)[0][1]
        print(f"\n🔮 Win Probability: {win_prob*100:.2f}%")

        # Get coaching suggestions
        print("📣 Coaching Advice:")
        print("👉 Suggested Bowler:", suggest_bowler(live_input["pitch"], live_input["run_rate"], live_input["required_rate"]))
        print("👉 Fielding Setup:", suggest_field(live_input["run_rate"], live_input["required_rate"]))
    except Exception as e:
        print(f"[ERROR] Could not complete live demo: {e}")

if __name__ == "__main__":
    print("🏏 AI Cricket Coach - Starting...\n")
    run_training()
    print("\n🚀 Running Live Match Analysis...\n")
    run_live_demo()
