import requests

def get_data():
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BTC&apikey=API_KEY."
    response = requests.get(url)
    values = response.json()
    print(values)
    return values
get_data()