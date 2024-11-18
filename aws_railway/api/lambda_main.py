import requests
import os

def get_data(event, context):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BTC&apikey=API_KEY."
    response = requests.get(url)
    values = response.json()
    print(values)
    return response
