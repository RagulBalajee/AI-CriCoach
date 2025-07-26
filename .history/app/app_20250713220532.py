# app/app.py
import streamlit as st
from scripts.strategy_engine import suggest_bowler, suggest_field_placement

st.title("AI Cricket Coach")
over = st.slider("Current Over", 1, 50)
score = st.number_input("Batsman Score")
pitch = st.selectbox("Pitch Type", ["dry", "green", "flat"])
run_rate = st.slider("Run Rate", 1.0, 10.0)
required = st.slider("Required Run Rate", 1.0, 10.0)

st.write("Suggested Bowler:", suggest_bowler(over, score, pitch))
st.write("Suggested Fielding:", suggest_field_placement(run_rate, required))
