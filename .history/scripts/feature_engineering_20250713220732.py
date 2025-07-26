import pandas as pd

def load_data(path):
    return pd.read_csv(path)

def engineer_features(df):
    df['run_rate'] = df['runs'] / df['overs']
    df['wicket_rate'] = df['wickets'] / df['overs']
    return df[['overs','score','wickets','run_rate','wicket_rate','target_remaining']]
