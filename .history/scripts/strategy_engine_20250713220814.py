def suggest_bowler(pitch, current_run_rate, required_rate):
    if pitch=='dry' and current_run_rate > required_rate:
        return "Bring in spinner"
    if pitch=='green':
        return "Use fast bowler"
    return "Medium pacer should work"

def suggest_field(current_run_rate, required_rate):
    return "Spreading field" if current_run_rate > required_rate else "Crowded infield"
