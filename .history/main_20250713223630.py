# main.py

import pandas as pd
from scripts.feature_engineering import load_data, engineer_features
from scripts.predictor import train_model, load_model
from scripts.strategy_engine import suggest_bowler, suggest_field

def run_training():
    try:
        df = load_data("data/deliveries.csv", "data/ipl_matches.csv")
        print("[INFO] Data loaded successfully.")

        df_features = engineer_features(df)
        print("[INFO] Feature engineering complete.")

        df_features = df_features.dropna()  # clean up
        train_model(df_features)

        print("[✅] Model trained and saved to models/win_pred.pkl")

    except FileNotFoundError as e:
        print(f"[❌] File not found: {e}")
    except Exception as e:
        print(f"[❌] Error during training: {e}")

def run_live_demo():
    try:
        model = load_model()
        print("[INFO] Model loaded successfully.")

        # 🏏 Simulated live match scenario
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

        # ✅ Use DataFrame with matching column names
        features = pd.DataFrame([[
            live_input["overs"],
            live_input["score"],
            live_input["wickets"],
            live_input["run_rate"],
            live_input["wicket_rate"],
            live_input["target_remaining"]
        ]], columns=["overs", "score", "wickets", "run_rate", "wicket_rate", "target_remaining"])

        # 🔮 Predict win probability
        win_prob = model.predict_proba(features)[0][1]
        print(f"\n🔮 Win Probability: {win_prob * 100:.2f}%")

        # 🧠 AI Coaching Advice
        print("\n📣 Coaching Suggestions:")
        print("👉 Suggested Bowler:", suggest_bowler(live_input["pitch"], live_input["run_rate"], live_input["required_rate"]))
        print("👉 Fielding Strategy:", suggest_field(live_input["run_rate"], live_input["required_rate"]))

    except FileNotFoundError:
        print("[❌] Model file not found. Run training first.")
    except Exception as e:
        print(f"[❌] Live demo failed: {e}")

if __name__ == "__main__":
    print("🏏 AI Cricket Coach - Starting...\n")
    run_training()
    print("\n🚀 Running Live Match Analysis...\n")
    run_live_demo()
