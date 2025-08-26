import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

# --- Load Data from Database ---
def load_data_from_db(db_name, table_name):
    """Loads data from the SQLite database."""
    engine = create_engine(f'sqlite:///{db_name}')
    df = pd.read_sql_table(table_name, engine)
    df['date'] = pd.to_datetime(df['date']) # Ensure date is in datetime format
    return df

try:
    df = load_data_from_db('weather_database.db', 'clean_weather')
except Exception as e:
    print(f"Error loading data: {e}")
    print("Please run `etl_pipeline.py` first to create the database.")
    df = pd.DataFrame() # Create empty dataframe to avoid app crash

# --- Initialize the Dash App ---
app = dash.Dash(__name__)
app.title = "Weather Data Dashboard"

# --- Create Figures ---
if not df.empty:
    # Figure 1: Temperature Trend Over Time
    fig_temp_trend = px.line(
        df, 
        x='date', 
        y='temperature_fahrenheit', 
        color='city',
        title='Temperature Trend (Fahrenheit)',
        labels={'temperature_fahrenheit': 'Temperature (°F)', 'date': 'Date'}
    )
    
    # Figure 2: Average Humidity by City
    avg_humidity = df.groupby('city')['humidity_percent'].mean().reset_index()
    fig_avg_humidity = px.bar(
        avg_humidity,
        x='city',
        y='humidity_percent',
        title='Average Humidity by City',
        labels={'humidity_percent': 'Average Humidity (%)', 'city': 'City'}
    )
    
    # Figure 3: Wind Speed vs. Precipitation
    fig_wind_precip = px.scatter(
        df,
        x='wind_speed_kmh',
        y='precipitation_mm',
        color='city',
        size='precipitation_mm',
        hover_data=['date'],
        title='Wind Speed vs. Precipitation',
        labels={'wind_speed_kmh': 'Wind Speed (km/h)', 'precipitation_mm': 'Precipitation (mm)'}
    )
else:
    # Create empty figures if data loading failed
    fig_temp_trend = {}
    fig_avg_humidity = {}
    fig_wind_precip = {}

# --- App Layout ---
app.layout = html.Div(children=[
    html.H1(children='Weather Data Dashboard', style={'textAlign': 'center'}),

    html.Div(children='''
        An interactive dashboard to visualize the cleaned weather data.
    ''', style={'textAlign': 'center'}),

    dcc.Graph(
        id='temperature-trend-graph',
        figure=fig_temp_trend
    ),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Graph(
                id='avg-humidity-graph',
                figure=fig_avg_humidity
            )
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(
                id='wind-precip-scatter',
                figure=fig_wind_precip
            )
        ]),
    ], style={'display': 'flex'})
])

# --- Run the App ---
if __name__ == '__main__':
    if not df.empty:
        app.run(debug=True)
    else:
        print("Could not start dashboard because data is not available.")