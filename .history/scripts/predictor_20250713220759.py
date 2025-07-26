import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def train_model(df):
    X = df[['overs','score','wickets','run_rate','wicket_rate','target_remaining']]
    y = df['win']
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)
    print("Accuracy:", model.score(X_test, y_test))
    joblib.dump(model, "../models/win_pred.pkl")

def load_model():
    return joblib.load("../models/win_pred.pkl")
