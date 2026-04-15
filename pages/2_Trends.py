import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px

# Set the page configuration
st.set_page_config(layout="wide", page_title="Trends & Insights")

# Title of the trends page
st.title("Trends & Insights")

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

# Calculate summary statistics for selected columns
summary_stats = filtered_df[['Recovery_Score', 'Sleep_Hours', 'Steps', 'Calories_Burned']].agg(['mean', 'min', 'max'])

# Display summary statistics
st.write("### Summary Statistics")
st.dataframe(summary_stats.style.format(precision=2))

# Monthly average Recovery Score as a line chart
filtered_df['Month'] = filtered_df['Date'].dt.to_period('M')
monthly_avg_recovery = filtered_df.groupby('Month')['Recovery_Score'].mean().reset_index()

# Convert period to string for JSON serialization
monthly_avg_recovery['Month'] = monthly_avg_recovery['Month'].astype(str)

fig_avg_recovery_monthly = px.line(
    monthly_avg_recovery, x='Month', y='Recovery_Score',
    labels={'Recovery_Score': 'Average Recovery Score', 'Month': 'Month'},
    title="Average Recovery Score by Month"
)

st.plotly_chart(fig_avg_recovery_monthly, use_container_width=True)

# Histograms for the distribution of steps, calories burned, recovery score, and sleep hours
for column in ['Steps', 'Calories_Burned', 'Recovery_Score', 'Sleep_Hours']:
    fig_histogram = px.histogram(
        filtered_df, x=column,
        title=f"Distribution of {column.replace('_', ' ')}",
        labels={column: column.replace('_', ' ')}
    )
    st.plotly_chart(fig_histogram, use_container_width=True)

# The layout is designed to provide deeper insights into personal health trends over chosen time periods.