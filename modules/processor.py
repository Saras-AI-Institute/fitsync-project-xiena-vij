# New function to calculate Recovery_Score

def calculate_recovery_score(df):
    """
    Adds a 'Recovery_Score' column to the DataFrame, representing the daily recovery score (0 to 100).

    Args:
        df (pd.DataFrame): DataFrame containing health data.

    Returns:
        pd.DataFrame: Modified DataFrame with the new 'Recovery_Score' column.
    """
    # Initialize scores based on Sleep_Hours, Heart_Rate_bpm, and Steps
    
    def score_sleep_hours(hours):
        """Assign recovery score based on sleep hours."""
        if hours >= 7:
            return 30  # Good sleep
        elif hours >= 6:
            return 20  # Adequate sleep
        else:
            return 0   # Poor sleep

    def score_heart_rate(bpm):
        """Assign recovery score based on heart rate."""
        if bpm < 60:
            return 30  # Excellent heart rate
        elif bpm <= 75:
            return 20  # Good heart rate
        else:
            return 10  # Average heart rate

    def score_steps(steps):
        """Assign recovery score based on steps taken."""
        if steps < 5000:
            return 10  # Low activity
        elif steps <= 10000:
            return 20  # Moderate activity
        else:
            return 10  # High activity can cause strain

    # Calculate Recovery_Score
    scores = []
    for _, row in df.iterrows():
        sleep_score = score_sleep_hours(row['Sleep_Hours'])
        heart_score = score_heart_rate(row['Heart_Rate_bpm'])
        steps_score = score_steps(row['Steps'])
        
        # Calculate total recovery score
        total_score = sleep_score + heart_score + steps_score

        # Ensure score is between 0 to 100
        total_score = min(max(total_score, 0), 100)
        
        # Append to the scores list
        scores.append(total_score)

    # Add Recovery_Score to DataFrame
    df['Recovery_Score'] = scores

    return df
