# DataPipeline


# Data Pipeline with ETL & Visualization
This project demonstrates a complete, yet simple, Extract, Transform, Load (ETL) pipeline. It processes raw weather data from a CSV file, cleans and transforms it, loads the clean data into an SQLite database, and then visualizes the results in an interactive web dashboard.

# Tech Stack:

Python: The core language for the pipeline.

Pandas: For data manipulation and transformation.

SQLAlchemy: To interact with the SQL database.

SQLite: A lightweight, file-based database perfect for demonstration.

Plotly Dash: To build and serve the interactive web dashboard for visualization.

# Project Structure

etl-data-pipeline/
├── etl_pipeline.py       # The main script for the ETL process
├── dashboard.py          # The script for the Plotly Dash app
├── weather_data.csv      # The raw, messy sample data
├── weather_database.db   # The SQLite database (created by the ETL script)
├── requirements.txt
└── README.md

# How It Works

Extract: The etl_pipeline.py script reads the raw data from weather_data.csv.

Transform: It performs several cleaning and transformation steps:

Handles missing values.

Converts temperature from Celsius to Fahrenheit.

Corrects data types.

Creates a new "condition" column based on precipitation.

Load: The cleaned and transformed data is saved into a table named clean_weather inside the weather_database.db SQLite file.

Visualize: The dashboard.py script reads the clean data from the database and presents it in an interactive dashboard with various charts.
