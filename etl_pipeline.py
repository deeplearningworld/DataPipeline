import pandas as pd
from sqlalchemy import create_engine

def extract_data(file_path):
    """Extracts data from a CSV file."""
    print("Extracting data...")
    return pd.read_csv(file_path)

def transform_data(df):
    """Cleans and transforms the weather data."""
    print("Transforming data...")
    # Handle missing values
    df['temperature_celsius'].fillna(df['temperature_celsius'].median(), inplace=True)
    df['humidity_percent'].fillna(df['humidity_percent'].median(), inplace=True)
    df['wind_speed_kmh'].fillna(df['wind_speed_kmh'].mean(), inplace=True)
    df['precipitation_mm'].fillna(0.0, inplace=True)

    # Correct data types
    df['date'] = pd.to_datetime(df['date'])
    
    # Create new features
    df['temperature_fahrenheit'] = (df['temperature_celsius'] * 9/5) + 32
    
    def get_condition(precip):
        if precip == 0.0:
            return 'Clear'
        elif 0.0 < precip <= 2.5:
            return 'Light Rain/Snow'
        else:
            return 'Heavy Rain/Snow'
    
    df['condition'] = df['precipitation_mm'].apply(get_condition)
    
    # Ensure column names are clean
    df.columns = df.columns.str.strip()
    
    print("Transformation complete.")
    return df

def load_data(df, db_name, table_name):
    """Loads the transformed data into an SQLite database."""
    print(f"Loading data into {db_name}...")
    engine = create_engine(f'sqlite:///{db_name}')
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print("Data loaded successfully.")

def run_pipeline(csv_path, db_name, table_name):
    """Runs the full ETL pipeline."""
    # Extract
    raw_df = extract_data(csv_path)
    
    # Transform
    clean_df = transform_data(raw_df)
    
    # Load
    load_data(clean_df, db_name, table_name)
    
    print("\nETL Pipeline Finished!")
    print("Clean data is now in the SQLite database.")
    print("First 5 rows of the clean data:")
    print(clean_df.head())

if __name__ == "__main__":
    run_pipeline(
        csv_path='weather_data.csv',
        db_name='weather_database.db',
        table_name='clean_weather'
    )