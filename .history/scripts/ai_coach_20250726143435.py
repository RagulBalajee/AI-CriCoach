import sys
import pandas as pd
from scripts.predictor import load_model
from scripts.strategy_engine import suggest_bowler, suggest_field
import csv
import os

def get_user_input():
    print("Welcome to the Enhanced AI Cricket Coach!")
    match_type = input("Enter match type (T20/ODI/Test): ").strip().lower()
    pitch = input("Enter pitch type (dry, green, dusty, flat, etc.): ").strip().lower()
    weather = input("Enter weather conditions (sunny, cloudy, humid, dew, etc.): ").strip().lower()
    day_night = input("Is it a day or night match? (day/night): ").strip().lower()
    opposition = input("Opposition strength? (strong/average/weak): ").strip().lower()
    try:
        runs = int(input("Enter current runs: "))
        wickets = int(input("Enter wickets lost: "))
        overs = float(input("Enter overs completed: "))
        if match_type == "test":
            balls_left = None  # Not relevant for Test matches
            overs_remaining = None
            innings = int(input("Enter current innings (1 or 2): "))
            day = int(input("Enter current day (1-5): "))
            session = input("Enter session (morning/afternoon/evening): ").strip().lower()
        else:
            overs_remaining = float(input("Enter overs remaining in the innings: "))
            balls_left = int(overs_remaining * 6)
            innings = 1
            day = 1
            session = ""
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
    return (match_type, pitch, weather, day_night, opposition, runs, wickets, overs, balls_left, target, role, player_type, balls_faced, runs_conceded, overs_bowled, innings, day, session)

def calculate_features_for_prediction(runs, wickets, overs, target):
    run_rate = runs / overs if overs > 0 else 0
    wicket_rate = wickets / overs if overs > 0 else 0
    target_remaining = (target - runs) if target is not None else 200 - runs
    return pd.DataFrame([[overs, runs, wickets, run_rate, wicket_rate, target_remaining]],
                        columns=["overs", "score", "wickets", "run_rate", "wicket_rate", "target_remaining"])

def give_advice(match_type, pitch, weather, day_night, opposition, runs, wickets, overs, balls_left, target, role, player_type, balls_faced, runs_conceded, overs_bowled, innings, day, session):
    advice = ""
    scold = ""
    motivational = ""
    # Game phase
    if match_type == "test":
        if session:
            advice += f"Session: {session.capitalize()}. "
        if day:
            advice += f"Day {day}. "
        if innings == 1:
            advice += "First innings: Set a strong total. "
        elif innings == 2:
            advice += "Second innings: Consider match situation, pitch wear, and time left. "
        if overs < 30:
            phase = "morning"
        elif overs < 60:
            phase = "afternoon"
        else:
            phase = "evening"
    else:
        if overs < 6:
            phase = "powerplay"
        elif overs < 16:
            phase = "middle"
        else:
            phase = "death"
    # Required run rate
    required_run_rate = None
    if target is not None and balls_left is not None and balls_left > 0:
        runs_needed = target - runs
        required_run_rate = (runs_needed / balls_left) * 6
    # Batting advice
    if role == "batting":
        if match_type == "test":
            if wickets < 3 and overs < 30:
                advice += "Build a solid foundation, leave balls outside off, tire the bowlers. "
            elif wickets >= 7:
                advice += "Protect your wicket, bat for time, and avoid risky shots. "
            elif runs/overs > 3.5:
                advice += "Great scoring rate for Tests! Keep rotating strike. "
            else:
                advice += "Look for singles, build partnerships, and tire the fielders. "
            if day >= 4 and innings == 2 and target is not None:
                advice += "Chasing in the 4th innings: Watch for pitch deterioration and play for a draw if needed. "
            if session == "evening":
                advice += "Be extra cautious, light may fade and bowlers may get a second wind. "
        else:
            if pitch in ["green", "dusty"]:
                advice += "Be cautious, the pitch may help bowlers. "
            elif pitch == "flat":
                advice += "Good batting conditions, play positively. "
            elif pitch == "dry":
                advice += "Watch for spin as the game progresses. "
            if wickets < 3 and overs < 10:
                advice += "Build a solid foundation, avoid risky shots early. "
            elif wickets >= 7:
                advice += "Protect your wicket, rotate strike, and bat out the overs. "
            elif runs/overs > 7:
                advice += "Great run rate! Keep the momentum but don't lose wickets. "
            else:
                advice += "Look for singles, build partnerships, and accelerate later. "
            if required_run_rate:
                advice += f"Required run rate is {required_run_rate:.2f}. "
                if required_run_rate > 9:
                    advice += "Look for boundaries, but don't panic. "
                elif required_run_rate < 6:
                    advice += "Take singles, avoid unnecessary risks. "
        # Scolding
        if balls_faced and balls_faced > 0:
            strike_rate = (runs / balls_faced) * 100
            if match_type == "test" and strike_rate < 40:
                scold += f"Strike rate is too low for Test ({strike_rate:.1f})! Rotate the strike and tire the bowlers! "
            elif match_type != "test" and strike_rate < 70:
                scold += f"Strike rate is too low ({strike_rate:.1f})! Pick up the pace! "
        if overs > 0:
            run_rate = runs / overs
            if match_type == "test" and run_rate < 2:
                scold += f"Scoring rate is very slow ({run_rate:.1f})! Don't get stuck, but value your wicket. "
            elif match_type != "test" and run_rate < 4:
                scold += f"Run rate is too slow ({run_rate:.1f})! Rotate the strike and look for boundaries! "
        # Motivational
        if wickets >= 7:
            motivational += "Stay calm under pressure, every run counts! "
        elif match_type == "test" and day >= 4 and innings == 2 and target is not None:
            motivational += "History is made in the 4th innings! Stay focused, play session by session! "
        else:
            motivational += "Keep your focus, play to your strengths! "
    # Bowling advice
    elif role == "bowling":
        if match_type == "test":
            if pitch in ["green"]:
                advice += "Use seamers, pitch the ball up, exploit morning conditions. "
            elif pitch in ["dusty", "dry"]:
                advice += "Bring spinners early, use variations, and attack rough patches. "
            elif pitch == "flat":
                advice += "Focus on line and length, set attacking fields, and be patient. "
            if session == "morning":
                advice += "Attack with slips and close fielders, new ball may swing. "
            elif session == "evening":
                advice += "Use reverse swing, keep fielders alert for tired batters. "
            if day >= 4 and innings == 4:
                advice += "Pitch may break up, spinners can be match-winners. "
        else:
            if pitch in ["green"]:
                advice += "Use seamers, pitch the ball up. "
            elif pitch in ["dusty", "dry"]:
                advice += "Bring spinners early, use variations. "
            elif pitch == "flat":
                advice += "Focus on line and length, set defensive fields. "
            if overs < 10:
                advice += "Attack with slips and close fielders. "
            elif wickets < 3:
                advice += "Try to break partnerships, use attacking fields. "
            elif runs/overs > 8:
                advice += "Set defensive fields, bowl to your field, and vary pace. "
            else:
                advice += "Keep building pressure, force mistakes. "
        # Scolding
        if runs_conceded is not None and overs_bowled and overs_bowled > 0:
            run_rate_conceded = runs_conceded / overs_bowled
            if match_type == "test" and run_rate_conceded > 4:
                scold += f"Conceding runs too quickly for Test ({run_rate_conceded:.1f})! Focus on patience and accuracy! "
            elif match_type != "test" and run_rate_conceded > 6:
                scold += f"Bowling run rate is too high ({run_rate_conceded:.1f})! Bowl tighter lines and stick to the plan! "
        # Motivational
        if wickets < 3 and match_type == "test" and session == "evening":
            motivational += "One wicket can change the session! Stay sharp! "
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

def log_scenario_result(log_path, context):
    file_exists = os.path.isfile(log_path)
    with open(log_path, mode='a', newline='') as csvfile:
        fieldnames = list(context.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(context)

def get_team_venue_stats(team=None, venue=None, matches_path="data/ipl_matches.csv"):
    try:
        matches = pd.read_csv(matches_path)
        advice = ""
        if team:
            total = len(matches[(matches['team1'] == team) | (matches['team2'] == team)])
            wins = len(matches[matches['winner'] == team])
            if total > 0:
                win_rate = wins / total * 100
                advice += f"{team} historical win rate: {win_rate:.1f}% in IPL. "
        if venue:
            venue_matches = matches[matches['venue'].str.lower() == venue.lower()]
            if not venue_matches.empty:
                venue_win_counts = venue_matches['winner'].value_counts()
                top_team = venue_win_counts.idxmax()
                top_wins = venue_win_counts.max()
                advice += f"At {venue}, {top_team} has the most wins ({top_wins}). "
        return advice
    except Exception as e:
        return f"[❌] Error fetching team/venue stats: {e}"

def main():
    model = load_model()
    (
        match_type, pitch, weather, day_night, opposition, runs, wickets, overs, balls_left, target, role, player_type, balls_faced, runs_conceded, overs_bowled, innings, day, session
    ) = get_user_input()
    team = input("Enter your team name (optional): ").strip()
    venue = input("Enter venue/stadium (optional): ").strip()
    print("\n==============================")
    print("🏏 \033[1mAI Cricket Coach\033[0m")
    print("==============================\n")
    advice, scold, motivational = give_advice(
        match_type, pitch, weather, day_night, opposition, runs, wickets, overs, balls_left, target, role, player_type, balls_faced, runs_conceded, overs_bowled, innings, day, session
    )
    features = calculate_features_for_prediction(runs, wickets, overs, target)
    try:
        win_prob = model.predict_proba(features)[0][1]
        print(f"\033[1m🔮 Win Probability:\033[0m {win_prob * 100:.2f}%\n")
    except Exception as e:
        print(f"[❌] Win probability prediction failed: {e}\n")
    print(f"\033[1m📣 Coach's Advice:\033[0m {advice}")
    if team or venue:
        print(f"\033[1m🏟️ Team/Venue Stats:\033[0m {get_team_venue_stats(team, venue)}")
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
    # Log initial scenario
    log_scenario_result("scenario_log.csv", {
        "team": team,
        "venue": venue,
        "pitch": pitch,
        "weather": weather,
        "day_night": day_night,
        "opposition": opposition,
        "runs": runs,
        "wickets": wickets,
        "overs": overs,
        "balls_left": balls_left,
        "target": target,
        "role": role,
        "player_type": player_type,
        "advice": advice,
        "scold": scold,
        "motivational": motivational,
        "win_prob": win_prob if 'win_prob' in locals() else None
    })
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
            venue = input("Enter new venue/stadium: ").strip()
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
                venue = input("Enter venue/stadium: ").strip()
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
            match_type, pitch, weather, day_night, opposition, runs, wickets, overs, balls_left, target, role, player_type, balls_faced, runs_conceded, overs_bowled, innings, day, session
        )
        features = calculate_features_for_prediction(runs, wickets, overs, target)
        try:
            win_prob = model.predict_proba(features)[0][1]
            print(f"\033[1m🔮 [Scenario] Win Probability:\033[0m {win_prob * 100:.2f}%\n")
        except Exception as e:
            print(f"[❌] Win probability prediction failed: {e}\n")
        print(f"\033[1m📣 [Scenario] Coach's Advice:\033[0m {advice}")
        if team or venue:
            print(f"\033[1m🏟️ [Scenario] Team/Venue Stats:\033[0m {get_team_venue_stats(team, venue)}")
        if scold:
            print(f"\033[91m⚠️ [Scenario] Coach's Scolding:\033[0m {scold}")
        if motivational:
            print(f"\033[94m💡 [Scenario] Coach's Motivation:\033[0m {motivational}")
        print("\n\033[1m🧠 [Scenario] Unique Suggestions:\033[0m")
        print("👉 Best Bowler:", suggest_bowler(pitch, run_rate, required_rate))
        print("👉 Fielding Strategy:", suggest_field(run_rate, required_rate))
        print("\n\033[1m📚 [Scenario] Historical Match Insight:\033[0m")
        print(find_similar_match(runs, wickets, overs, target))
        # Log scenario
        log_scenario_result("scenario_log.csv", {
            "team": team,
            "venue": venue,
            "pitch": pitch,
            "weather": weather,
            "day_night": day_night,
            "opposition": opposition,
            "runs": runs,
            "wickets": wickets,
            "overs": overs,
            "balls_left": balls_left,
            "target": target,
            "role": role,
            "player_type": player_type,
            "advice": advice,
            "scold": scold,
            "motivational": motivational,
            "win_prob": win_prob if 'win_prob' in locals() else None
        })

if __name__ == "__main__":
    main() 