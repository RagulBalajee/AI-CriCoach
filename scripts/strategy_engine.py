# scripts/strategy_engine.py

def suggest_bowler(pitch_type, run_rate, required_rate):
    if pitch_type == "dry":
        return "Leg spinner" if run_rate > required_rate else "Off spinner"
    elif pitch_type == "green":
        return "Fast bowler"
    elif pitch_type == "dusty":
        return "Left-arm orthodox"
    else:
        return "Medium pacer"

def suggest_field(run_rate, required_rate):
    if run_rate > required_rate:
        return "Defensive field with deep cover and long-off"
    elif run_rate < required_rate:
        return "Aggressive field with slip, short leg, and mid-on"
    else:
        return "Balanced field with one sweeper and inner ring"
