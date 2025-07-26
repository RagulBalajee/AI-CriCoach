import sys
import pandas as pd
from scripts.predictor import load_model
from scripts.strategy_engine import suggest_bowler, suggest_field

def get_user_input():
    print("Welcome to the Enhanced AI Cricket Coach!")
    pitch = input("Enter pitch type (dry, green, dusty, flat, etc.): ").strip().lower()
    weather = input("Enter weather conditions (sunny, cloudy, humid, dew, etc.): ").strip().lower()
    day_night = input("Is it a day or night match? (day/night): ").strip().lower()
    opposition = input("Opposition strength? (strong/average/weak): ").strip().lower()
    try:
        runs = int(input("Enter current runs: "))
        wickets = int(input("Enter wickets lost: "))
        overs = float(input("Enter overs completed: "))
        balls_left = int(input("Enter balls left in the innings: "))
    except ValueError:
        print("Invalid input for score. Please enter numbers.")
        sys.exit(1)
    target = input("Are you chasing a target? Enter target score or 'none': ").strip().lower()
    if target != 'none':
        try:
            target = int(target)
        except ValueError:
            print("Invalid input for target. Please enter a number or 'none'.")
            sys.exit(1)
    else:
        target = None
    role = input("Are you Batting or Bowling? (batting/bowling): ").strip().lower()
    player_type = input("What type of player/bowler are you? (aggressive/anchor/spinner/pacer/allrounder): ").strip().lower()
    balls_faced = None
    runs_conceded = None
    overs_bowled = None
    if role == "batting":
        try:
            balls_faced = int(input("Enter balls faced: "))
        except ValueError:
            print("Invalid input for balls faced. Please enter a number.")
            sys.exit(1)
    elif role == "bowling":
        try:
            runs_conceded = int(input("Enter runs conceded: "))
            overs_bowled = float(input("Enter overs bowled: "))
        except ValueError:
            print("Invalid input for bowling stats. Please enter numbers.")
            sys.exit(1)
    return (pitch, weather, day_night, opposition, runs, wickets, overs, balls_left, target, role, player_type, balls_faced, runs_conceded, overs_bowled)

def calculate_features_for_prediction(runs, wickets, overs, target):
    run_rate = runs / overs if overs > 0 else 0
    wicket_rate = wickets / overs if overs > 0 else 0
    target_remaining = (target - runs) if target is not None else 200 - runs
    return pd.DataFrame([[overs, runs, wickets, run_rate, wicket_rate, target_remaining]],
                        columns=["overs", "score", "wickets", "run_rate", "wicket_rate", "target_remaining"])

def give_advice(pitch, weather, day_night, opposition, runs, wickets, overs, balls_left, target, role, player_type, balls_faced, runs_conceded, overs_bowled):
    advice = ""
    scold = ""
    motivational = ""
    # Game phase
    if overs < 6:
        phase = "powerplay"
    elif overs < 16:
        phase = "middle"
    else:
        phase = "death"
    # Required run rate
    required_run_rate = None
    if target is not None and balls_left > 0:
        runs_needed = target - runs
        required_run_rate = (runs_needed / balls_left) * 6
    # Batting advice
    if role == "batting":
        if pitch in ["green", "dusty"]:
            advice += "Be cautious, the pitch may help bowlers. "
        elif pitch == "flat":
            advice += "Good batting conditions, play positively. "
        elif pitch == "dry":
            advice += "Watch for spin as the game progresses. "
        if weather in ["humid", "dew"]:
            advice += "Ball may swing or get wet, adjust accordingly. "
        if day_night == "night" and weather == "dew":
            advice += "Dew may make it hard for bowlers to grip, take advantage. "
        if opposition == "strong":
            advice += "Respect good bowlers, target weaker ones. "
        elif opposition == "weak":
            advice += "Dominate the bowling, but don't get complacent. "
        # Player type
        if player_type == "aggressive":
            advice += "Back your shots, but pick the right balls. "
        elif player_type == "anchor":
            advice += "Hold the innings together, rotate strike. "
        # Game phase
        if phase == "powerplay":
            advice += "Exploit fielding restrictions, but don't lose early wickets. "
        elif phase == "middle":
            advice += "Build partnerships, rotate strike, and set up for the finish. "
        else:
            advice += "Accelerate, but keep wickets in hand for the last overs. "
        # Required run rate
        if required_run_rate:
            advice += f"Required run rate is {required_run_rate:.2f}. "
            if required_run_rate > 9:
                advice += "Look for boundaries, but don't panic. "
            elif required_run_rate < 6:
                advice += "Take singles, avoid unnecessary risks. "
        # Scolding
        if balls_faced and balls_faced > 0:
            strike_rate = (runs / balls_faced) * 100
            if strike_rate < 70:
                scold += f"Strike rate is too low ({strike_rate:.1f})! Pick up the pace! "
        if overs > 0:
            run_rate = runs / overs
            if run_rate < 4:
                scold += f"Run rate is too slow ({run_rate:.1f})! Rotate the strike and look for boundaries! "
        # Motivational
        if wickets >= 7:
            motivational += "Stay calm under pressure, every run counts! "
        elif required_run_rate and required_run_rate > 10:
            motivational += "Believe in yourself, matches have been won from tougher situations! "
        else:
            motivational += "Keep your focus, play to your strengths! "
    # Bowling advice
    elif role == "bowling":
        if pitch in ["green"]:
            advice += "Use seamers, pitch the ball up. "
        elif pitch in ["dusty", "dry"]:
            advice += "Bring spinners early, use variations. "
        elif pitch == "flat":
            advice += "Focus on line and length, set defensive fields. "
        if weather == "humid":
            advice += "Look for swing, especially early. "
        if day_night == "night" and weather == "dew":
            advice += "Ball may be slippery, use spinners or bowlers with good control. "
        if opposition == "strong":
            advice += "Attack their best batters early, set aggressive fields. "
        elif opposition == "weak":
            advice += "Don't relax, stick to your plans. "
        # Player type
        if player_type == "spinner":
            advice += "Vary your pace and flight, use the crease. "
        elif player_type == "pacer":
            advice += "Bowl full and straight, use bouncers wisely. "
        # Game phase
        if phase == "powerplay":
            advice += "Attack with slips and close fielders. "
        elif phase == "middle":
            advice += "Build pressure, bowl tight lines. "
        else:
            advice += "Use yorkers and slower balls, protect boundaries. "
        # Scolding
        if runs_conceded is not None and overs_bowled and overs_bowled > 0:
            run_rate_conceded = runs_conceded / overs_bowled
            if run_rate_conceded > 6:
                scold += f"Bowling run rate is too high ({run_rate_conceded:.1f})! Bowl tighter lines and stick to the plan! "
        # Motivational
        if wickets < 3 and phase == "death":
            motivational += "Wickets now can turn the game! Stay sharp! "
        else:
            motivational += "Keep your composure, bowl to your field! "
    else:
        advice = "Invalid role. Please enter 'batting' or 'bowling'."
    return advice, scold, motivational

def find_similar_match(runs, wickets, overs, target, matches_path="data/ipl_matches.csv"):
    try:
        matches = pd.read_csv(matches_path)
        # Filter only matches with a similar target (±10 runs)
        if target is not None:
            similar = matches[(matches['target_runs'].notnull()) & (abs(matches['target_runs'] - target) <= 10)]
        else:
            similar = matches
        # Find matches with similar runs/wickets/overs (±10 runs, ±1 wicket, ±1 over)
        similar = similar[(abs(similar['target_runs'] - runs) <= 10) & (abs(similar['target_overs'] - overs) <= 1)]
        if not similar.empty:
            match = similar.sample(1).iloc[0]
            return f"In {match['season']} at {match['venue']}, {match['team1']} vs {match['team2']}: Target {match['target_runs']}, Result: {match['winner']} won by {match['result_margin']} {match['result']}."
        else:
            return "No close historical match found."
    except Exception as e:
        return f"[❌] Error finding historical match: {e}"

def main():
    model = load_model()
    (
        pitch, weather, day_night, opposition, runs, wickets, overs, balls_left, target, role, player_type, balls_faced, runs_conceded, overs_bowled
    ) = get_user_input()
    print("\n==============================")
    print("🏏 \033[1mAI Cricket Coach\033[0m")
    print("==============================\n")
    advice, scold, motivational = give_advice(
        pitch, weather, day_night, opposition, runs, wickets, overs, balls_left, target, role, player_type, balls_faced, runs_conceded, overs_bowled
    )
    features = calculate_features_for_prediction(runs, wickets, overs, target)
    try:
        win_prob = model.predict_proba(features)[0][1]
        print(f"\033[1m🔮 Win Probability:\033[0m {win_prob * 100:.2f}%\n")
    except Exception as e:
        print(f"[❌] Win probability prediction failed: {e}\n")
    print(f"\033[1m📣 Coach's Advice:\033[0m {advice}")
    if scold:
        print(f"\033[91m⚠️ Coach's Scolding:\033[0m {scold}")
    if motivational:
        print(f"\033[94m💡 Coach's Motivation:\033[0m {motivational}")
    print("\n\033[1m🧠 Unique Suggestions:\033[0m")
    run_rate = runs / overs if overs > 0 else 0
    required_rate = (target - runs) / (20 - overs) if (target is not None and overs < 20 and (20 - overs) > 0) else run_rate
    print("👉 Best Bowler:", suggest_bowler(pitch, run_rate, required_rate))
    print("👉 Fielding Strategy:", suggest_field(run_rate, required_rate))
    print("\n\033[1m📚 Historical Match Insight:\033[0m")
    print(find_similar_match(runs, wickets, overs, target))
    # Scenario simulation
    while True:
        print("\n==============================")
        print("🧩 \033[1mScenario Simulation Menu\033[0m 🧩")
        print("==============================")
        simulate = input("Would you like to simulate a scenario? (yes/no): ").strip().lower()
        if simulate != "yes":
            print("\n🎉 Thank you for using the AI Cricket Coach! 🏏")
            break
        print("\n--- Scenario Simulation Options ---")
        print("  1️⃣  Lose a wicket")
        print("  2️⃣  Score a boundary")
        print("  3️⃣  Bowl a maiden")
        print("  4️⃣  Add 10 runs")
        print("  5️⃣  Lose 2 wickets")
        print("  6️⃣  Powerplay over (add 6 balls, 8 runs)")
        print("  7️⃣  Death over (add 6 balls, 12 runs)")
        print("  8️⃣  Rain interruption (skip 2 overs)")
        print("  9️⃣  Change player type")
        print(" 10️⃣  Change opposition strength")
        print(" 11️⃣  Change venue")
        print(" 12️⃣  Change weather")
        print(" 13️⃣  Player injury (lose a key player)")
        print(" 14️⃣  Super over (reset overs to 0, balls left to 6, wickets to 2, runs to 0)")
        print(" 15️⃣  Custom scenario (set all values)")
        option = input("Choose an option (1-15): ").strip()
        if option == "1":
            wickets += 1
            balls_left -= 1
        elif option == "2":
            runs += 4
            balls_left -= 1
        elif option == "3":
            overs += 1/6
            balls_left -= 6
        elif option == "4":
            runs += 10
            balls_left -= 2
        elif option == "5":
            wickets += 2
            balls_left -= 2
        elif option == "6":
            overs += 1
            runs += 8
            balls_left -= 6
        elif option == "7":
            overs += 1
            runs += 12
            balls_left -= 6
        elif option == "8":
            overs += 2
            balls_left -= 12
            print("🌧️ Rain interruption! 2 overs lost.")
        elif option == "9":
            player_type = input("Enter new player type (aggressive/anchor/spinner/pacer/allrounder): ").strip().lower()
        elif option == "10":
            opposition = input("Enter new opposition strength (strong/average/weak): ").strip().lower()
        elif option == "11":
            pitch = input("Enter new pitch/venue type (dry/green/dusty/flat/etc.): ").strip().lower()
        elif option == "12":
            weather = input("Enter new weather (sunny/cloudy/humid/dew/etc.): ").strip().lower()
        elif option == "13":
            print("🚑 Player injury! Losing a key player may impact morale and performance.")
            motivational = "Stay strong as a team, adapt to the challenge!"
            wickets += 1
            balls_left -= 1
        elif option == "14":
            print("🔥 Super Over! Resetting scenario...")
            overs = 0
            balls_left = 6
            wickets = 2
            runs = 0
        elif option == "15":
            try:
                runs = int(input("Enter new runs: "))
                wickets = int(input("Enter new wickets: "))
                overs = float(input("Enter new overs: "))
                balls_left = int(input("Enter new balls left: "))
                player_type = input("Enter player type (aggressive/anchor/spinner/pacer/allrounder): ").strip().lower()
                opposition = input("Enter opposition strength (strong/average/weak): ").strip().lower()
                pitch = input("Enter pitch/venue type (dry/green/dusty/flat/etc.): ").strip().lower()
                weather = input("Enter weather (sunny/cloudy/humid/dew/etc.): ").strip().lower()
            except ValueError:
                print("Invalid input. Returning to main menu.")
                continue
        else:
            print("Invalid option. Returning to main menu.")
            continue
        print("\n==============================")
        print("🧩 \033[1mScenario Results\033[0m 🧩")
        print("==============================")
        advice, scold, motivational = give_advice(
            pitch, weather, day_night, opposition, runs, wickets, overs, balls_left, target, role, player_type, balls_faced, runs_conceded, overs_bowled
        )
        features = calculate_features_for_prediction(runs, wickets, overs, target)
        try:
            win_prob = model.predict_proba(features)[0][1]
            print(f"\033[1m🔮 [Scenario] Win Probability:\033[0m {win_prob * 100:.2f}%\n")
        except Exception as e:
            print(f"[❌] Win probability prediction failed: {e}\n")
        print(f"\033[1m📣 [Scenario] Coach's Advice:\033[0m {advice}")
        if scold:
            print(f"\033[91m⚠️ [Scenario] Coach's Scolding:\033[0m {scold}")
        if motivational:
            print(f"\033[94m💡 [Scenario] Coach's Motivation:\033[0m {motivational}")
        print("\n\033[1m🧠 [Scenario] Unique Suggestions:\033[0m")
        print("👉 Best Bowler:", suggest_bowler(pitch, run_rate, required_rate))
        print("👉 Fielding Strategy:", suggest_field(run_rate, required_rate))
        print("\n\033[1m📚 [Scenario] Historical Match Insight:\033[0m")
        print(find_similar_match(runs, wickets, overs, target))

if __name__ == "__main__":
    main() 