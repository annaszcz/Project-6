import requests

def get_data():
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BTC&apikey=B6EHIX42BOYPDA9B."
    response = requests.get(url)
    values = response.json()
    print(values)
    return values
get_data()