# main.py
from scripts.strategy_engine import suggest_bowler, suggest_field_placement
from scripts.data_scraper import get_live_score

live_data = {
    "over": 12,
    "batsman_score": 30,
    "pitch_type": "dry",
    "run_rate": 7.5,
    "required_rate": 8.2
}

print("Live Score:", get_live_score())
print("Suggest Bowler:", suggest_bowler(live_data["over"], live_data["batsman_score"], live_data["pitch_type"]))
print("Field Placement:", suggest_field_placement(live_data["run_rate"], live_data["required_rate"]))
