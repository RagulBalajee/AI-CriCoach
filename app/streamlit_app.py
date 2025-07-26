import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.ai_coach import give_advice, calculate_features_for_prediction, load_model, find_similar_match, get_team_venue_stats
from scripts.strategy_engine import suggest_bowler, suggest_field

st.set_page_config(page_title="AI Cricket Coach", page_icon="🏏", layout="wide")

# Modern CSS: animated background, glassmorphism, fonts, icons, transitions
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Roboto:wght@400;500&display=swap');
body, .stApp {
  background: linear-gradient(120deg, #e0eafc 0%, #cfdef3 100%);
  background-size: 400% 400%;
  animation: gradientBG 12s ease infinite;
  font-family: 'Roboto', sans-serif;
}
@keyframes gradientBG {
  0% {background-position: 0% 50%;}
  50% {background-position: 100% 50%;}
  100% {background-position: 0% 50%;}
}
.hero {
  background: rgba(30,144,255,0.85);
  backdrop-filter: blur(2px);
  padding: 2.5rem 1rem 1.5rem 1rem;
  border-radius: 1.5rem;
  margin-bottom: 2rem;
  text-align: center;
  color: white;
  font-family: 'Montserrat', sans-serif;
  animation: fadein 1.2s;
  box-shadow: 0 4px 32px rgba(30,144,255,0.18);
}
.hero-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
  font-family: 'Montserrat', sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5em;
}
.hero-sub {
  font-size: 1.3rem;
  font-weight: 400;
  margin-bottom: 0.5rem;
  font-family: 'Roboto', sans-serif;
}
.card {
  background: rgba(255,255,255,0.75);
  border-radius: 1.2rem;
  box-shadow: 0 2px 24px rgba(30,144,255,0.13);
  padding: 1.5rem 2rem;
  margin-bottom: 1.5rem;
  transition: box-shadow 0.3s, background 0.3s;
  animation: fadein 1.2s;
  backdrop-filter: blur(8px);
}
.card:hover {
  box-shadow: 0 8px 40px rgba(30,144,255,0.22);
  background: rgba(255,255,255,0.92);
}
.card-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #1e90ff;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5em;
}
.badge {
  display: inline-block;
  padding: 0.3em 0.8em;
  border-radius: 1em;
  font-size: 1em;
  font-weight: 500;
  margin-right: 0.5em;
  margin-bottom: 0.2em;
}
.badge-advice { background: #e0f7fa; color: #00796b; }
.badge-motivation { background: #fff3e0; color: #e65100; }
.badge-warning { background: #ffebee; color: #b71c1c; }
.fadein { animation: fadein 1.2s; }
@keyframes fadein { from { opacity: 0; transform: translateY(30px);} to { opacity: 1; transform: none; } }
.sticky-footer {
  position: fixed;
  left: 0; right: 0; bottom: 0;
  background: #1e90ff;
  color: white;
  text-align: center;
  padding: 0.5rem 0;
  font-size: 1rem;
  z-index: 100;
}
.fab {
  position: fixed;
  bottom: 2.5rem;
  right: 2.5rem;
  background: #1e90ff;
  color: white;
  border-radius: 50%;
  width: 60px; height: 60px;
  display: flex; align-items: center; justify-content: center;
  font-size: 2rem;
  box-shadow: 0 4px 16px rgba(30,144,255,0.18);
  cursor: pointer;
  border: none;
  z-index: 200;
  transition: background 0.2s;
}
.fab:hover { background: #00c3ff; }
</style>
<div class="hero fadein">
  <div class="hero-title">
    <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="20" cy="20" r="18" fill="#fff" stroke="#1e90ff" stroke-width="3"/><circle cx="20" cy="20" r="12" fill="#ff9800" stroke="#fff" stroke-width="2"/><circle cx="20" cy="20" r="6" fill="#43a047"/></svg>
    AI Cricket Coach
  </div>
  <div class="hero-sub">Cricket strategy, powered by AI.<br>T20, ODI, and Test match support · Real-time scenario simulation · Win probability, historical insights, and more</div>
  <a href="https://github.com/RagulBalajee/AI-CriCoach" style="color:#fff; text-decoration:underline; font-size:1rem;">GitHub Repo</a>
</div>
""", unsafe_allow_html=True)

with st.form("match_form"):
    st.markdown('<div class="card fadein"><div class="card-title">📝 <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="4" width="20" height="16" rx="4" fill="#1e90ff" fill-opacity="0.12"/><rect x="4" y="6" width="16" height="12" rx="2" fill="#fff"/></svg> Match Details</div>', unsafe_allow_html=True)
    match_type = st.selectbox("Match type", ["T20", "ODI", "Test"])
    col1, col2 = st.columns(2)
    with col1:
        pitch = st.selectbox("Pitch type", ["dry", "green", "dusty", "flat", "other"])
        weather = st.selectbox("Weather", ["sunny", "cloudy", "humid", "dew", "other"])
        day_night = st.selectbox("Day or night match?", ["day", "night"])
        opposition = st.selectbox("Opposition strength", ["strong", "average", "weak"])
    with col2:
        runs = st.number_input("Current runs", min_value=0, value=0)
        wickets = st.number_input("Wickets lost", min_value=0, max_value=10, value=0)
        overs = st.number_input("Overs completed", min_value=0.0, value=0.0, step=0.1)
    if match_type.lower() == "test":
        balls_left = None
        overs_remaining = None
        innings = st.selectbox("Current innings", [1, 2])
        day = st.slider("Current day", 1, 5, 1)
        session = st.selectbox("Session", ["morning", "afternoon", "evening"])
    else:
        overs_remaining = st.number_input("Overs remaining in the innings", min_value=0.0, value=0.0, step=0.1)
        balls_left = int(overs_remaining * 6)
        innings = 1
        day = 1
        session = ""
    target = st.text_input("Target score (or 'none' if not chasing)", value="none")
    if target.strip().lower() != "none":
        try:
            target = int(target)
        except:
            st.warning("Please enter a valid number for target or 'none'.")
            st.stop()
    else:
        target = None
    col3, col4 = st.columns(2)
    with col3:
        role = st.selectbox("Are you Batting or Bowling?", ["batting", "bowling"])
        player_type = st.selectbox("Player/Bowler type", ["aggressive", "anchor", "spinner", "pacer", "allrounder"])
        balls_faced = st.number_input("Balls faced (batting only)", min_value=0, value=0) if role == "batting" else None
    with col4:
        runs_conceded = st.number_input("Runs conceded (bowling only)", min_value=0, value=0) if role == "bowling" else None
        overs_bowled = st.number_input("Overs bowled (bowling only)", min_value=0.0, value=0.0, step=0.1) if role == "bowling" else None
        team = st.text_input("Your team name (optional)")
        venue = st.text_input("Venue/stadium (optional)")
    submit = st.form_submit_button("Get Coaching Advice 🏏")
    st.markdown('</div>', unsafe_allow_html=True)

if submit:
    if 'scenario' not in st.session_state or st.session_state.get('reset', False):
        st.session_state['scenario'] = {
            'match_type': match_type.lower(),
            'pitch': pitch,
            'weather': weather,
            'day_night': day_night,
            'opposition': opposition,
            'runs': runs,
            'wickets': wickets,
            'overs': overs,
            'balls_left': balls_left,
            'target': target,
            'role': role,
            'player_type': player_type,
            'balls_faced': balls_faced,
            'runs_conceded': runs_conceded,
            'overs_bowled': overs_bowled,
            'innings': innings,
            'day': day,
            'session': session,
            'team': team,
            'venue': venue
        }
        st.session_state['reset'] = False
    scenario = st.session_state['scenario']
    # Recalculate outputs for the current scenario
    model = load_model()
    impossible_chase = False
    if scenario['match_type'] != "test" and scenario['target'] is not None and scenario['balls_left'] is not None:
        runs_needed = scenario['target'] - scenario['runs']
        if runs_needed > scenario['balls_left'] * 6:
            impossible_chase = True
    # Calculate run rates for rule-based override
    run_rate = scenario['runs'] / scenario['overs'] if scenario['overs'] > 0 else 0
    required_rate = (scenario['target'] - scenario['runs']) / (20 - scenario['overs']) if (scenario['target'] is not None and scenario['overs'] < 20 and (20 - scenario['overs']) > 0) else run_rate
    # Rule-based win probability override
    rule_override = False
    if not impossible_chase and scenario['match_type'] != "test":
        if (run_rate > required_rate + 2) and (scenario['wickets'] <= 2) and (scenario['overs'] < 15):
            win_prob = 0.9
            rule_override = True
        elif (run_rate < required_rate - 2) and (scenario['wickets'] >= 7):
            win_prob = 0.1
            rule_override = True
    if impossible_chase:
        win_prob = 0.0
        advice = "This match cannot be won. Play for pride, enjoy the last balls, and try to finish strong!"
        scold = ""
        motivational = "Give your best till the last ball!"
    elif rule_override:
        if win_prob == 0.9:
            advice = "You are in a dominant position! Keep up the momentum, play smart, and finish strong."
            scold = "Don't get complacent—cricket can change quickly!"
            motivational = "Victory is within reach! Stay focused."
        elif win_prob == 0.1:
            advice = "This is a tough situation. Play for pride, look for partnerships, and try to take the game deep."
            scold = "You need a miracle! Don't give up, but be realistic."
            motivational = "Cricket is a game of surprises—fight till the end!"
        else:
            advice = "Play to the situation."
            scold = ""
            motivational = "Give your best!"
    else:
        advice, scold, motivational = give_advice(
            scenario['match_type'], scenario['pitch'], scenario['weather'], scenario['day_night'], scenario['opposition'], scenario['runs'], scenario['wickets'], scenario['overs'], scenario['balls_left'], scenario['target'], scenario['role'], scenario['player_type'], scenario['balls_faced'], scenario['runs_conceded'], scenario['overs_bowled'], scenario['innings'], scenario['day'], scenario['session']
        )
        features = calculate_features_for_prediction(scenario['runs'], scenario['wickets'], scenario['overs'], scenario['target'])
        try:
            win_prob = model.predict_proba(features)[0][1]
        except Exception as e:
            st.error(f"Win probability prediction failed: {e}")
            win_prob = None
    st.markdown('<div class="card fadein">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🔮 <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" fill="#fff" stroke="#1e90ff" stroke-width="2"/><circle cx="12" cy="12" r="6" fill="#ff9800" stroke="#fff" stroke-width="2"/></svg> Win Probability</div>', unsafe_allow_html=True)
    st.progress(win_prob if win_prob is not None else 0.0)
    st.markdown(f"<span style='font-size:2rem; color:#1e90ff;'><b>{win_prob * 100:.2f}%</b></span>" if win_prob is not None else "N/A", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="card fadein">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📣 <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="4" width="20" height="16" rx="4" fill="#1e90ff" fill-opacity="0.12"/><rect x="4" y="6" width="16" height="12" rx="2" fill="#fff"/></svg> Coach\'s Advice</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="badge badge-advice">Advice</span> {advice}', unsafe_allow_html=True)
    if scenario['team'] or scenario['venue']:
        st.markdown('<div class="card-title">🏟️ <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="4" width="20" height="16" rx="4" fill="#43a047" fill-opacity="0.12"/><rect x="4" y="6" width="16" height="12" rx="2" fill="#fff"/></svg> Team/Venue Stats</div>', unsafe_allow_html=True)
        st.write(get_team_venue_stats(scenario['team'], scenario['venue']))
    if scold:
        st.markdown(f'<span class="badge badge-warning">Warning</span> {scold}', unsafe_allow_html=True)
    if motivational:
        st.markdown(f'<span class="badge badge-motivation">Motivation</span> {motivational}', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    with st.expander("🧠 Unique Suggestions", expanded=True):
        run_rate = scenario['runs'] / scenario['overs'] if scenario['overs'] > 0 else 0
        required_rate = (scenario['target'] - scenario['runs']) / (20 - scenario['overs']) if (scenario['target'] is not None and scenario['overs'] < 20 and (20 - scenario['overs']) > 0) else run_rate
        st.write(f"👉 Best Bowler: {suggest_bowler(scenario['pitch'], run_rate, required_rate)}")
        st.write(f"👉 Fielding Strategy: {suggest_field(run_rate, required_rate)}")
    with st.expander("📚 Historical Match Insight", expanded=True):
        st.write(find_similar_match(scenario['runs'], scenario['wickets'], scenario['overs'], scenario['target']))
    # Scenario simulation UI (moved to bottom)
    st.markdown('<div class="card fadein">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🧩 <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" fill="#fff" stroke="#1e90ff" stroke-width="2"/><rect x="7" y="7" width="10" height="10" rx="2" fill="#1e90ff" fill-opacity="0.12"/></svg> Scenario Simulation</div>', unsafe_allow_html=True)
    st.caption("Simulate match events to see updated advice and probabilities:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Lose a wicket"):
            scenario['wickets'] += 1
            if scenario['balls_left'] is not None:
                scenario['balls_left'] -= 1
    with col2:
        if st.button("Score a boundary"):
            scenario['runs'] += 4
            if scenario['balls_left'] is not None:
                scenario['balls_left'] -= 1
    with col3:
        if st.button("Bowl a maiden"):
            scenario['overs'] += 1/6
            if scenario['balls_left'] is not None:
                scenario['balls_left'] -= 6
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("Add 10 runs"):
            scenario['runs'] += 10
            if scenario['balls_left'] is not None:
                scenario['balls_left'] -= 2
    with col5:
        if st.button("Lose 2 wickets"):
            scenario['wickets'] += 2
            if scenario['balls_left'] is not None:
                scenario['balls_left'] -= 2
    with col6:
        if st.button("Powerplay over"):
            scenario['overs'] += 1
            scenario['runs'] += 8
            if scenario['balls_left'] is not None:
                scenario['balls_left'] -= 6
    col7, col8, col9 = st.columns(3)
    with col7:
        if st.button("Death over"):
            scenario['overs'] += 1
            scenario['runs'] += 12
            if scenario['balls_left'] is not None:
                scenario['balls_left'] -= 6
    with col8:
        if st.button("Rain interruption"):
            scenario['overs'] += 2
            if scenario['balls_left'] is not None:
                scenario['balls_left'] -= 12
    with col9:
        if st.button("Player injury"):
            scenario['wickets'] += 1
            if scenario['balls_left'] is not None:
                scenario['balls_left'] -= 1
    if st.button("Super over"):
        scenario['overs'] = 0
        scenario['balls_left'] = 6
        scenario['wickets'] = 2
        scenario['runs'] = 0
    if st.button("Custom scenario"):
        scenario['runs'] = st.number_input("Custom: Enter new runs", min_value=0, value=scenario['runs'], key='custom_runs')
        scenario['wickets'] = st.number_input("Custom: Enter new wickets", min_value=0, max_value=10, value=scenario['wickets'], key='custom_wickets')
        scenario['overs'] = st.number_input("Custom: Enter new overs", min_value=0.0, value=scenario['overs'], step=0.1, key='custom_overs')
        if scenario['match_type'] != 'test':
            scenario['balls_left'] = st.number_input("Custom: Enter new balls left", min_value=0, value=scenario['balls_left'] or 0, key='custom_balls_left')
        scenario['player_type'] = st.selectbox("Custom: Player type", ["aggressive", "anchor", "spinner", "pacer", "allrounder"], index=["aggressive", "anchor", "spinner", "pacer", "allrounder"].index(scenario['player_type']), key='custom_player_type')
        scenario['opposition'] = st.selectbox("Custom: Opposition strength", ["strong", "average", "weak"], index=["strong", "average", "weak"].index(scenario['opposition']), key='custom_opposition')
        scenario['pitch'] = st.selectbox("Custom: Pitch type", ["dry", "green", "dusty", "flat", "other"], index=["dry", "green", "dusty", "flat", "other"].index(scenario['pitch']), key='custom_pitch')
        scenario['weather'] = st.selectbox("Custom: Weather", ["sunny", "cloudy", "humid", "dew", "other"], index=["sunny", "cloudy", "humid", "dew", "other"].index(scenario['weather']), key='custom_weather')
        scenario['venue'] = st.text_input("Custom: Venue/stadium", value=scenario['venue'], key='custom_venue')
        scenario['team'] = st.text_input("Custom: Team name", value=scenario['team'], key='custom_team')
        st.session_state['reset'] = True
        st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Floating action button for reset
st.markdown('''<button class="fab" onclick="window.location.reload();" title="Reset Scenario">⟳</button>''', unsafe_allow_html=True) 