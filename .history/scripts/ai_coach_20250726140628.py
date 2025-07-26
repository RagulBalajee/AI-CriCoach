import sys

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

def main():
    (
        pitch, weather, day_night, opposition, runs, wickets, overs, balls_left, target, role, player_type, balls_faced, runs_conceded, overs_bowled
    ) = get_user_input()
    advice, scold, motivational = give_advice(
        pitch, weather, day_night, opposition, runs, wickets, overs, balls_left, target, role, player_type, balls_faced, runs_conceded, overs_bowled
    )
    print(f"\nCoach's Advice: {advice}")
    if scold:
        print(f"\nCoach's Scolding: {scold}")
    if motivational:
        print(f"\nCoach's Motivation: {motivational}")

if __name__ == "__main__":
    main() 