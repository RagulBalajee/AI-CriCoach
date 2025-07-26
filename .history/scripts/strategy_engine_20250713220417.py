# scripts/strategy_engine.py
def suggest_bowler(current_over, batsman_score, pitch_type):
    if pitch_type == "dry":
        return "Spin bowler"
    elif pitch_type == "green":
        return "Fast bowler"
    else:
        return "Medium pace"

def suggest_field_placement(run_rate, required_rate):
    if run_rate < required_rate:
        return "Aggressive field"
    else:
        return "Defensive field"
