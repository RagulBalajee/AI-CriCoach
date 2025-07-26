from flask import Flask, jsonify, request
from scripts.predictor import load_model
from scripts.strategy_engine import suggest_bowler, suggest_field

app = Flask(__name__)
model = load_model()

@app.route("/predict", methods=["POST"])
def predict():
    d = request.json
    prob = model.predict_proba([[
        d['overs'], d['score'], d['wickets'],
        d['run_rate'], d['wicket_rate'], d['target_remaining']
    ]])[0][1]
    return jsonify({"win_prob": prob})

@app.route("/advise", methods=["POST"])
def advise():
    d = request.json
    return jsonify({
        "bowler": suggest_bowler(d['pitch'], d['run_rate'], d['required_rate']),
        "field": suggest_field(d['run_rate'], d['required_rate'])
    })

if __name__=="__main__":
    app.run(debug=True)
