import streamlit as st
from modules.processor import process_data
from modules.theme import apply_theme, style_fig, metric_card, section_header, page_banner
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="FitSync - Dashboard", page_icon="📊")

theme = apply_theme("dashboard")
T = theme

gradient = "linear-gradient(135deg, #1f3a5f 0%, #0d2137 100%)" if T["is_dark"] else "linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%)"
page_banner("📊 FitSync Dashboard", "Your personal health metrics at a glance", gradient, T)

@st.cache_data
def get_processed_data():
    return process_data()

# process_data function call modified with caching
df = get_processed_data()

st.sidebar.markdown(f"<div style='font-size:18px; font-weight:700; margin-bottom:16px;'>⚙️ Filters</div>", unsafe_allow_html=True)
time_range = st.sidebar.selectbox("Select Time Range", ["Last 7 Days", "Last 30 Days", "All Time"], index=2)

if time_range == "Last 7 Days":
    filtered_df = df[df['Date'] > df['Date'].max() - pd.Timedelta(days=7)]
elif time_range == "Last 30 Days":
    filtered_df = df[df['Date'] > df['Date'].max() - pd.Timedelta(days=30)]
else:
    filtered_df = df

avg_steps    = filtered_df['Steps'].mean()
avg_sleep    = filtered_df['Sleep_Hours'].mean()
avg_recovery = filtered_df['Recovery_Score'].mean()
avg_calories = filtered_df['Calories_Burned'].mean()

section_header("📌 Key Metrics", T)
c1, c2, c3, c4 = st.columns(4)
with c1: metric_card("Average Steps",    f"{avg_steps:,.0f}",    "🚶", "#58a6ff", T)
with c2: metric_card("Sleep Hours",      f"{avg_sleep:.1f} hrs", "😴", "#3fb950", T)
with c3: metric_card("Recovery Score",   f"{avg_recovery:.1f}",  "💚", "#d2a8ff", T)
with c4: metric_card("Calories Burned",  f"{avg_calories:,.0f}", "🔥", "#f78166", T)

section_header("📈 Trends Over Time", T)
left1, right1 = st.columns(2)

with left1:
    fig = px.line(filtered_df, x='Date', y=['Recovery_Score', 'Sleep_Hours'],
                  labels={'value': 'Score / Hours', 'Date': 'Date'},
                  title="🛌 Recovery Score & Sleep Trend",
                  color_discrete_sequence=["#58a6ff", "#3fb950"])
    st.plotly_chart(style_fig(fig, T), use_container_width=True)

with right1:
    fig = px.scatter(filtered_df, x='Steps', y='Recovery_Score', color='Sleep_Hours',
                     labels={'Steps': 'Daily Steps', 'Recovery_Score': 'Recovery Score'},
                     title="🚶 Recovery Score vs Daily Steps",
                     color_continuous_scale="Blues")
    st.plotly_chart(style_fig(fig, T), use_container_width=True)

section_header("🔍 Deep Dive", T)
left2, right2 = st.columns(2)

with left2:
    fig = px.scatter(filtered_df, x='Heart_Rate_bpm', y='Recovery_Score',
                     labels={'Heart_Rate_bpm': 'Resting Heart Rate (bpm)', 'Recovery_Score': 'Recovery Score'},
                     title="❤️ Recovery Score vs Resting Heart Rate",
                     color_discrete_sequence=["#f78166"])
    st.plotly_chart(style_fig(fig, T), use_container_width=True)

with right2:
    fig = px.line(filtered_df, x='Date', y='Calories_Burned',
                  labels={'Calories_Burned': 'Calories Burned', 'Date': 'Date'},
                  title="🔥 Daily Calories Burned Trend",
                  color_discrete_sequence=["#d2a8ff"])
    fig.add_hrect(
        y0=filtered_df['Calories_Burned'].mean() * 0.95,
        y1=filtered_df['Calories_Burned'].mean() * 1.05,
        fillcolor="#d2a8ff", opacity=0.08, line_width=0,
        annotation_text="avg zone"
    )
    st.plotly_chart(style_fig(fig, T), use_container_width=True)