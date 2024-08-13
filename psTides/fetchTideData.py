import requests
import json
from datetime import datetime, timedelta

# Calculate the date range
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
end_date = (datetime.now() + timedelta(days=7)).strftime('%Y%m%d')

# NOAA Tides and Currents API URL
api_url = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter'
params = {
    'product': 'predictions',
    'application': 'NOS.COOPS.TAC.WL',
    'begin_date': yesterday,
    'end_date': end_date,
    'datum': 'MLLW',
    #Everett:
    'station': '9447659', 
    #Seattle: '9447130',
    'time_zone': 'lst_ldt',
    'units': 'english',
    'interval': 'hilo',
    'format': 'json'
}

response = requests.get(api_url, params=params)
data = response.json()

# Save data to a JSON file
with open('tide_data.json', 'w') as f:
    json.dump(data, f, indent=4)
