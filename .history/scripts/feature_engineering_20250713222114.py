import pandas as pd

def load_data(deliveries_path, matches_path):
    deliveries = pd.read_csv(deliveries_path)
    matches = pd.read_csv(matches_path)

    # Prepare deliveries data
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
    df['run_rate'] = df['score'] / df['overs']
    df['wicket_rate'] = df.groupby(['match_id'])['wickets'].cumsum() / df['overs']
    df['target_remaining'] = 200 - df['score']  # Simulated target of 200

    # Merge with match results
    matches = matches[['id', 'team1', 'team2', 'winner']]
    df = df.merge(matches, how='left', left_on='match_id', right_on='id')

    # Label: did team1 win?
    df['win'] = (df['team1'] == df['winner']).astype(int)

    return df[['overs', 'score', 'wickets', 'run_rate', 'wicket_rate', 'target_remaining', 'win']]
