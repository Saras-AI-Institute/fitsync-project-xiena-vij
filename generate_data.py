import pandas as pd
import numpy as np
from datetime import timedelta, date

# Function to generate date range
def generate_date_range(start_date, num_days):
    return [start_date + timedelta(days=i) for i in range(num_days)]

# Function to introduce missing values
def introduce_missing_values(data, missing_percent=0.05):
    total_values = data.size
    missing_values_count = int(total_values * missing_percent)
    missing_indices = np.random.choice(total_values, missing_values_count, replace=False)
    flat_data = data.to_numpy().flatten()
    flat_data[missing_indices] = np.nan
    return pd.DataFrame(flat_data.reshape(data.shape), columns=data.columns)

# Seed for reproducibility
np.random.seed(42)

# Generate 365 days of data starting from 2025-01-01
dates = generate_date_range(start_date=date(2025, 1, 1), num_days=365)

# Generate columns with realistic data
steps = np.random.normal(loc=8500, scale=2000, size=365).clip(3000, 18000)
sleep_hours = np.random.normal(loc=7.2, scale=1.0, size=365).clip(4.5, 9.5)
heart_rate_bpm = np.random.normal(loc=68, scale=10, size=365).clip(48, 110)
calories_burned = np.random.uniform(1800, 4200, size=365)
active_minutes = np.random.uniform(20, 180, size=365)

# Create a DataFrame
fitness_data = pd.DataFrame({
    'Date': dates,
    'Steps': np.round(steps),
    'Sleep_Hours': np.round(sleep_hours, 1),
    'Heart_Rate_bpm': np.round(heart_rate_bpm),
    'Calories_Burned': np.round(calories_burned),
    'Active_Minutes': np.round(active_minutes)
})

# Introduce missing values
fitness_data_with_missing = introduce_missing_values(fitness_data)

# Save to CSV
fitness_data_with_missing.to_csv('data/health_data.csv', index=False)