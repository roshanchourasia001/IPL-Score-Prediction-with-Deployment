import streamlit as st
import pickle
import numpy as np

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Teams list
teams = [
    'Chennai Super Kings',
    'Delhi Daredevils',
    'Kings XI Punjab',
    'Kolkata Knight Riders',
    'Mumbai Indians',
    'Rajasthan Royals',
    'Royal Challengers Bangalore',
    'Sunrisers Hyderabad'
]

# Predict function
def predict_score(batting_team, bowling_team, overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5):
    batting_encoded = [1 if team == batting_team else 0 for team in teams]
    bowling_encoded = [1 if team == bowling_team else 0 for team in teams]
    features = batting_encoded + bowling_encoded + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
    features = np.array([features])
    return int(model.predict(features)[0])

# --- Streamlit UI ---
st.title("🏏 IPL Score Predictor")
st.markdown("Predict the final score based on current match situation")

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("🏏 Batting Team", teams)

with col2:
    bowling_team = st.selectbox("🎯 Bowling Team", [t for t in teams if t != batting_team])

st.divider()

col3, col4, col5 = st.columns(3)

with col3:
    overs = st.number_input("Overs Completed", min_value=5.1, max_value=19.5, value=5.1, step=0.1)

with col4:
    runs = st.number_input("Current Runs", min_value=0, max_value=300, value=50)

with col5:
    wickets = st.number_input("Wickets Fallen", min_value=0, max_value=9, value=0)

col6, col7 = st.columns(2)

with col6:
    runs_in_prev_5 = st.number_input("Runs in Last 5 Overs", min_value=0, max_value=150, value=30)

with col7:
    wickets_in_prev_5 = st.number_input("Wickets in Last 5 Overs", min_value=0, max_value=5, value=0)

st.divider()

if st.button("🔮 Predict Score", use_container_width=True):
    predicted = predict_score(batting_team, bowling_team, overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5)
    
    st.success(f"### 🏆 Predicted Final Score: {predicted - 5} - {predicted + 5}")
    
    col8, col9, col10 = st.columns(3)
    col8.metric("Low Estimate", predicted - 5)
    col9.metric("Predicted", predicted)
    col10.metric("High Estimate", predicted + 5)