# main.py

import pandas as pd
from scripts.feature_engineering import load_data, engineer_features
from scripts.predictor import train_model, load_model
from scripts.strategy_engine import suggest_bowler, suggest_field

def auto_calculate_features(score, overs, wickets, pitch, target=200):
    run_rate = score / overs if overs > 0 else 0
    wicket_rate = wickets / overs if overs > 0 else 0
    target_remaining = target - score
    overs_remaining = 20 - overs
    required_rate = target_remaining / overs_remaining if overs_remaining > 0 else 0

    return {
        "overs": overs,
        "score": score,
        "wickets": wickets,
        "run_rate": run_rate,
        "wicket_rate": wicket_rate,
        "target_remaining": target_remaining,
        "required_rate": required_rate,
        "pitch": pitch
    }

def run_training():
    try:
        df = load_data("data/deliveries.csv", "data/ipl_matches.csv")
        print("[INFO] Data loaded successfully.")
        df_features = engineer_features(df)
        print("[INFO] Feature engineering complete.")
        df_features = df_features.dropna()
        train_model(df_features)
        print("[✅] Model trained and saved to models/win_pred.pkl")
    except Exception as e:
        print(f"[❌] Training failed: {e}")

def run_live_demo():
    try:
        model = load_model()
        print("[INFO] Model loaded successfully.")

        # 👇 USER INPUT
        score = int(input("🏏 Enter current score: "))
        overs = float(input("⏱️ Enter overs completed: "))
        wickets = int(input("💥 Enter wickets lost: "))
        pitch = input("🌱 Enter pitch type (dry / flat / green): ").strip().lower()

        # 🔢 Auto calculate everything
        live_input = auto_calculate_features(score, overs, wickets, pitch)

        # 🧠 Build feature dataframe for prediction
        features = pd.DataFrame([[
            live_input["overs"],
            live_input["score"],
            live_input["wickets"],
            live_input["run_rate"],
            live_input["wicket_rate"],
            live_input["target_remaining"]
        ]], columns=["overs", "score", "wickets", "run_rate", "wicket_rate", "target_remaining"])

        # 🎯 Predict
        win_prob = model.predict_proba(features)[0][1]
        print(f"\n🔮 Win Probability: {win_prob * 100:.2f}%")

        print("\n📣 Coaching Suggestions:")
        print("👉 Best Bowler:", suggest_bowler(live_input["pitch"], live_input["run_rate"], live_input["required_rate"]))
        print("👉 Fielding Strategy:", suggest_field(live_input["run_rate"], live_input["required_rate"]))

    except Exception as e:
        print(f"[❌] Live analysis failed: {e}")

if __name__ == "__main__":
    print("🏏 AI Cricket Coach - Starting...\n")
    run_training()
    print("\n🚀 Running Live Match Analysis...\n")
    run_live_demo()
