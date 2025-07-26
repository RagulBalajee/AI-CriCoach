# scripts/feature_engineering.py

import pandas as pd

def load_data(deliveries_path, matches_path):
    deliveries = pd.read_csv(deliveries_path)
    matches = pd.read_csv(matches_path)

    # Summarize deliveries at over level
    df = deliveries.groupby(['match_id', 'inning', 'over']).agg({
        'total_runs': 'sum',
        'player_dismissed': 'count'
    }).reset_index()

    df = df.rename(columns={
        'total_runs': 'runs',
        'player_dismissed': 'wickets'
    })

    df['overs'] = df['over']
    df['score'] = df.groupby(['match_id'])['runs'].cumsum()

    # Avoid division by zero by filtering overs == 0
    df = df[df['overs'] != 0]

    df['run_rate'] = df['score'] / df['overs']
    df['wicket_rate'] = df.groupby(['match_id'])['wickets'].cumsum() / df['overs']
    df['target_remaining'] = 200 - df['score']  # simulated target

    # Merge with match results
    matches = matches[['id', 'team1', 'team2', 'winner']]
    df = df.merge(matches, how='left', left_on='match_id', right_on='id')

    # Binary label: Did team1 win?
    df['win'] = (df['team1'] == df['winner']).astype(int)

    return df

def engineer_features(df):
    features = df[['overs', 'score', 'wickets', 'run_rate', 'wicket_rate', 'target_remaining', 'win']].copy()

    # ✅ Clean the data
    features.replace([float('inf'), float('-inf')], pd.NA, inplace=True)
    features.dropna(inplace=True)

    return features
