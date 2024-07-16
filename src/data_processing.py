import os
import pandas as pd
import meteostat
from datetime import datetime

def download_and_preprocess_data(station_id):
    start = datetime(1900, 1, 1)
    end = datetime(2024, 12, 31)

    # Fetch data for the specified station
    data = meteostat.Daily(station_id, start, end)
    data = data.fetch()

    if not os.path.exists('data'):
        os.makedirs('data')

    data.to_csv('data/all_data.csv')
