import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px

# Set the page configuration
st.set_page_config(layout="wide", page_title="FitSync")

# Title of the dashboard
st.title("FitSync - Personal Health Analytics")

# Load and process the data
df = process_data()

# Add a sidebar header and time range filter
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)

# Filter the DataFrame based on the time range
if time_range == "Last 7 Days":
    date_threshold = df['Date'].max() - pd.Timedelta(days=7)
    filtered_df = df[df['Date'] > date_threshold]
elif time_range == "Last 30 Days":
    date_threshold = df['Date'].max() - pd.Timedelta(days=30)
    filtered_df = df[df['Date'] > date_threshold]
else:
    filtered_df = df

# Calculate metrics from the filtered data
avg_steps = filtered_df['Steps'].mean()
avg_sleep_hours = filtered_df['Sleep_Hours'].mean()
avg_recovery_score = filtered_df['Recovery_Score'].mean()

# Create a 3-column layout
col1, col2, col3 = st.columns(3)
# Display filtered metrics in columns
with col1:
    st.metric(label="Average Steps", value=f"{avg_steps:.0f}", delta=None)

with col2:
    st.metric(label="Average Sleep Hours", value=f"{avg_sleep_hours:.1f}", delta=None)

with col3:
    st.metric(label="Average Recovery Score", value=f"{avg_recovery_score:.1f}", delta=None)

# Create two columns for more visualizations
left_column_1, right_column_1 = st.columns(2)

# Left Column: Dual Line Chart for Recovery Score & Sleep Hours
with left_column_1:
    st.subheader("Recovery Score & Sleep Trend")
    fig_recovery_sleep = px.line(
        filtered_df, x='Date', y=['Recovery_Score', 'Sleep_Hours'],
        labels={'value': 'Score / Hours', 'Date': 'Date'},
        title="Recovery Score & Sleep Trend"
    )
    st.plotly_chart(fig_recovery_sleep, use_container_width=True)

# Right Column: Scatter Plot for Recovery Score vs Steps
with right_column_1:
    st.subheader("Recovery Score vs Daily Steps")
    fig_recovery_steps = px.scatter(
        filtered_df, x='Steps', y='Recovery_Score', color='Sleep_Hours',
        labels={'Steps': 'Daily Steps', 'Recovery_Score': 'Recovery Score', 'Sleep_Hours': 'Sleep Hours'},
        title="Recovery Score vs Daily Steps"
    )
    st.plotly_chart(fig_recovery_steps, use_container_width=True)

# Create another two columns for further visualizations
left_column_2, right_column_2 = st.columns(2)

# Left Column: Scatter Plot for Recovery Score vs Heart Rate
with left_column_2:
    st.subheader("Recovery Score vs Resting Heart Rate")
    fig_recovery_heart_rate = px.scatter(
        filtered_df, x='Heart_Rate_bpm', y='Recovery_Score',
        labels={'Heart_Rate_bpm': 'Resting Heart Rate (bpm)', 'Recovery_Score': 'Recovery Score'},
        title="Recovery Score vs Resting Heart Rate"
    )
    st.plotly_chart(fig_recovery_heart_rate, use_container_width=True)

# Right Column: Line Chart for Calories Burned over time
with right_column_2:
    st.subheader("Daily Calories Burned Trend")
    fig_calories_burned = px.line(
        filtered_df, x='Date', y='Calories_Burned',
        labels={'Calories_Burned': 'Calories Burned', 'Date': 'Date'},
        title="Daily Calories Burned Trend"
    )
    st.plotly_chart(fig_calories_burned, use_container_width=True)

# The layout is designed to be clean and professional with clear compartmentalization of metrics and visualizations.

