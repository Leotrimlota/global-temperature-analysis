import os
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
import numpy as np

def generate_plot():

    # Get the current working directory
    current_directory = os.getcwd()

    # Construct the full file path
    all_data_file_path = os.path.join(current_directory, 'data/all_data.csv')

    # Load the data, parsing dates
    all_data = pd.read_csv(all_data_file_path, parse_dates=['time'])

    # Extract the year from the date
    all_data['year'] = all_data['time'].dt.year

    # Group the data by year and calculate the mean, min, and max temperatures for each year
    yearly_avg_temp = all_data.groupby('year')['tavg'].mean().reset_index()
    yearly_min_temp = all_data.groupby('year')['tmin'].min().reset_index()
    yearly_max_temp = all_data.groupby('year')['tmax'].max().reset_index()

    # Merge the data into a single DataFrame
    yearly_temps = yearly_avg_temp.merge(yearly_min_temp, on='year').merge(yearly_max_temp, on='year')
    yearly_temps.rename(columns={'tavg': 'avg_temp', 'tmin': 'min_temp', 'tmax': 'max_temp'}, inplace=True)

    # Create a complete range of years
    all_years = pd.DataFrame({'year': np.arange(yearly_temps['year'].min(), yearly_temps['year'].max() + 1)})

    # Merge with the complete range of years to ensure all years are included
    yearly_temps = all_years.merge(yearly_temps, on='year', how='left')

    # Fill missing values with the mean of each column (or other appropriate value)
    yearly_temps['avg_temp'].fillna(yearly_temps['avg_temp'].mean(), inplace=True)
    yearly_temps['min_temp'].fillna(yearly_temps['min_temp'].mean(), inplace=True)
    yearly_temps['max_temp'].fillna(yearly_temps['max_temp'].mean(), inplace=True)

    # Create an interactive plot with Plotly
    fig = px.line(yearly_temps, x='year', y=['avg_temp', 'min_temp', 'max_temp'],
                labels={'value': 'Temperature (°C)', 'variable': 'Temperature Type'},
                title='Temperature Trends Over the Years')

    # Customize hover data to show year and temperature
    fig.update_traces(mode='lines+markers', hovertemplate='Year: %{x}<br>Temperature: %{y}°C')

    # Customize layout for grid and finer y-axis ticks
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            tick0=yearly_temps['year'].min(),
            dtick=1,
            showgrid=True
        ),
        yaxis=dict(
            tickmode='linear',
            tick0=yearly_temps[['avg_temp', 'min_temp', 'max_temp']].min().min(),
            dtick=5,
            showgrid=True
        ),
        plot_bgcolor='white'
    )

    # Ensure grid lines are visible
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    # Add linear trend lines for max_temp, avg_temp, and min_temp
    for temp_type in ['max_temp', 'avg_temp', 'min_temp']:
        X = sm.add_constant(yearly_temps['year'])  # Adds a constant term to the predictor
        model = sm.OLS(yearly_temps[temp_type], X).fit()
        yearly_temps[f'{temp_type}_trend'] = model.predict(X)

        # Add the trend line to the plot
        fig.add_traces(px.line(yearly_temps, x='year', y=f'{temp_type}_trend', 
                            labels={f'{temp_type}_trend': f'{temp_type.capitalize()} Trend'}).data)

    # Show the plot
    fig.show()
