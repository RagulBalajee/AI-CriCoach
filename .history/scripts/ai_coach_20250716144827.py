import sys

def get_user_input():
    print("Welcome to the AI Cricket Coach!")
    pitch = input("Enter pitch type (dry, green, dusty, flat, etc.): ").strip().lower()
    try:
        runs = int(input("Enter current runs: "))
        wickets = int(input("Enter wickets lost: "))
        overs = float(input("Enter overs completed: "))
    except ValueError:
        print("Invalid input for score. Please enter numbers.")
        sys.exit(1)
    role = input("Are you Batting or Bowling? (batting/bowling): ").strip().lower()
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
    return pitch, runs, wickets, overs, role, balls_faced, runs_conceded, overs_bowled

def give_advice(pitch, runs, wickets, overs, role, balls_faced, runs_conceded, overs_bowled):
    advice = ""
    scold = ""
    if role == "batting":
        # Advice
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
        # Scolding
        if balls_faced and balls_faced > 0:
            strike_rate = (runs / balls_faced) * 100
            if strike_rate < 70:
                scold += f"Strike rate is too low ({strike_rate:.1f})! Pick up the pace! "
        if overs > 0:
            run_rate = runs / overs
            if run_rate < 4:
                scold += f"Run rate is too slow ({run_rate:.1f})! Rotate the strike and look for boundaries! "
    elif role == "bowling":
        # Advice
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
            if run_rate_conceded > 6:
                scold += f"Bowling run rate is too high ({run_rate_conceded:.1f})! Bowl tighter lines and stick to the plan! "
    else:
        advice = "Invalid role. Please enter 'batting' or 'bowling'."
    return advice, scold

def main():
    pitch, runs, wickets, overs, role, balls_faced, runs_conceded, overs_bowled = get_user_input()
    advice, scold = give_advice(pitch, runs, wickets, overs, role, balls_faced, runs_conceded, overs_bowled)
    print(f"\nCoach's Advice: {advice}")
    if scold:
        print(f"\nCoach's Scolding: {scold}")

if __name__ == "__main__":
    main() 