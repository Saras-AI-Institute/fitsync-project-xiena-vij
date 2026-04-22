import streamlit as st
from modules.processor import process_data
from modules.theme import apply_theme, style_fig, section_header, page_banner
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="FitSync - Trends", page_icon="📈")

theme = apply_theme("trends")
T = theme

gradient = "linear-gradient(135deg, #0f3d20 0%, #0d2137 100%)" if T["is_dark"] else "linear-gradient(135deg, #dcfce7 0%, #eff6ff 100%)"
page_banner("📈 Trends & Insights", "Deeper analysis of your health patterns over time", gradient, T)

df = process_data()

st.sidebar.markdown(f"<div style='font-size:18px; font-weight:700; margin-bottom:16px;'>⚙️ Filters</div>", unsafe_allow_html=True)
time_range = st.sidebar.selectbox("Select Time Range", ["Last 7 Days", "Last 30 Days", "All Time"], index=2)

if time_range == "Last 7 Days":
    filtered_df = df[df['Date'] > df['Date'].max() - pd.Timedelta(days=7)]
elif time_range == "Last 30 Days":
    filtered_df = df[df['Date'] > df['Date'].max() - pd.Timedelta(days=30)]
else:
    filtered_df = df

# Summary stats
section_header("📋 Summary Statistics", T)
summary_stats = filtered_df[['Recovery_Score', 'Sleep_Hours', 'Steps', 'Calories_Burned']].agg(['mean', 'min', 'max'])

# Stat cards row
s_cols = st.columns(4)
stat_config = [
    ("Recovery Score", "💚", "#3fb950", "Recovery_Score"),
    ("Sleep Hours",    "😴", "#58a6ff", "Sleep_Hours"),
    ("Steps",          "🚶", "#d2a8ff", "Steps"),
    ("Calories",       "🔥", "#f78166", "Calories_Burned"),
]
for col, (label, emoji, color, key) in zip(s_cols, stat_config):
    with col:
        mean_val = summary_stats.loc['mean', key]
        min_val  = summary_stats.loc['min', key]
        max_val  = summary_stats.loc['max', key]
        st.markdown(f"""
        <div style="
            background-color: {T['card_bg']};
            border: 1px solid {T['border']};
            border-top: 3px solid {color};
            border-radius: 14px;
            padding: 18px 16px;
            box-shadow: {T['shadow']};
            text-align: center;
        ">
            <div style="font-size:26px;">{emoji}</div>
            <div style="font-size:13px; font-weight:700; color:{color} !important; margin:6px 0 4px;">{label}</div>
            <div style="font-size:20px; font-weight:800; color:{T['text']} !important;">{mean_val:,.1f}</div>
            <div style="font-size:11px; color:{T['subtext']} !important; margin-top:6px;">
                ↓ {min_val:,.1f} &nbsp;|&nbsp; ↑ {max_val:,.1f}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Monthly trend
section_header("📅 Monthly Recovery Trend", T)
filtered_df = filtered_df.copy()
filtered_df['Month'] = filtered_df['Date'].dt.to_period('M')
monthly_avg = filtered_df.groupby('Month')['Recovery_Score'].mean().reset_index()
monthly_avg['Month'] = monthly_avg['Month'].astype(str)

fig = px.area(monthly_avg, x='Month', y='Recovery_Score',
              markers=True,
              labels={'Recovery_Score': 'Avg Recovery Score', 'Month': 'Month'},
              title="📅 Average Recovery Score by Month",
              color_discrete_sequence=["#58a6ff"])
fig.update_traces(
    marker=dict(size=9, color="#58a6ff", line=dict(width=2, color="#0d1117")),
    line=dict(width=3),
    fillcolor="rgba(88,166,255,0.1)"
)
st.plotly_chart(style_fig(fig, T), use_container_width=True)

# Histograms in 2x2 grid
section_header("📊 Metric Distributions", T)

colors = {"Steps": "#58a6ff", "Calories_Burned": "#f78166",
          "Recovery_Score": "#3fb950", "Sleep_Hours": "#d2a8ff"}
emojis = {"Steps": "🚶", "Calories_Burned": "🔥",
          "Recovery_Score": "💚", "Sleep_Hours": "😴"}

row1 = st.columns(2)
row2 = st.columns(2)
grid = [
    (row1[0], "Steps"), (row1[1], "Calories_Burned"),
    (row2[0], "Recovery_Score"), (row2[1], "Sleep_Hours")
]

for col, column in grid:
    with col:
        fig = px.histogram(
            filtered_df, x=column, nbins=30,
            title=f"{emojis[column]} {column.replace('_', ' ')}",
            labels={column: column.replace('_', ' ')},
            color_discrete_sequence=[colors[column]]
        )
        fig.update_traces(marker_line_width=0, opacity=0.85)
        st.plotly_chart(style_fig(fig, T), use_container_width=True)