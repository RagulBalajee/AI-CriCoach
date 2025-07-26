from scripts.data_scraper import get_live_score_html
from scripts.feature_engineering import engineer_features, load_data
from scripts.predictor import train_model, load_model
from scripts.strategy_engine import suggest_bowler, suggest_field

def run_training():
    df = load_data("data/ipl_matches.csv")
    df = engineer_features(df)
    train_model(df)

def run_live_demo():
    score_text = get_live_score_html()
    print("Live score:", score_text)
    # Demo values
    pitch = 'dry'
    cur_rr, req_rr = 7.5, 8.3
    print("Bowler:", suggest_bowler(pitch, cur_rr, req_rr))
    print("Fielding plan:", suggest_field(cur_rr, req_rr))

if __name__=="__main__":
    run_training()
    run_live_demo()
