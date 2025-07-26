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
    return pitch, runs, wickets, overs, role

def give_advice(pitch, runs, wickets, overs, role):
    advice = ""
    if role == "batting":
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
    elif role == "bowling":
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
    else:
        advice = "Invalid role. Please enter 'batting' or 'bowling'."
    return advice

def main():
    pitch, runs, wickets, overs, role = get_user_input()
    advice = give_advice(pitch, runs, wickets, overs, role)
    print(f"\nCoach's Advice: {advice}")

if __name__ == "__main__":
    main() 