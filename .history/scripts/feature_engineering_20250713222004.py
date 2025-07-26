import pandas as pd

def load_data(path):
    return pd.read_csv(path)

def engineer_features(df):
    """
    Creates over-wise features like run rate, wickets per over, etc.
    """
    df_overwise = df.groupby(['match_id', 'inning', 'over']).agg({
        'total_runs': 'sum',
        'player_dismissed': 'count'
    }).reset_index()

    df_overwise = df_overwise.rename(columns={
        'total_runs': 'runs',
        'player_dismissed': 'wickets'
    })

    df_overwise['overs'] = df_overwise['over']
    df_overwise['score'] = df_overwise['runs'].cumsum()
    df_overwise['run_rate'] = df_overwise['score'] / df_overwise['overs']
    df_overwise['wicket_rate'] = df_overwise['wickets'].cumsum() / df_overwise['overs']
    df_overwise['target_remaining'] = 200 - df_overwise['score']  # Simulate a 200 target

    # Only select usable columns
    return df_overwise[['overs', 'score', 'wickets', 'run_rate', 'wicket_rate', 'target_remaining']]
