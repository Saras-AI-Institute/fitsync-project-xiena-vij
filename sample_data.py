import pandas as pd

def load_and_print_health_data():
    # Load the health_data.csv file
    df = pd.read_csv('data/health_data.csv')
    
    # Print the first 5 rows
    print("First 5 rows:")
    print(df.head())
    
    # Print the number of missing values in each column
    print("\nNumber of missing values in each column:")
    print(df.isnull().sum())

# Call the function to execute the script
if __name__ == "__main__":
    load_and_print_health_data()