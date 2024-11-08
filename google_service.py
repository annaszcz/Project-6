from main import get_data
import gspread
import pandas as pd


def save_data():
    # fetch data from api
    data = get_data()

    # transform data into dataframe with two columns: date, price (close)
    dates = []
    prices = []
    for date in data["Time Series (Daily)"]:
        dates.append(date)
        prices.append(data["Time Series (Daily)"][date]['4. close'])
    df = pd.DataFrame({ "date": dates, "price": prices })

    # connect to Google worksheet
    gc = gspread.service_account(filename="./service_account.json")
    worksheet = gc.open("API&Services").sheet1

    # update the Google worksheet
    worksheet.update(values=[df.columns.values.tolist()] + df.values.tolist(), range_name='my_range')
save_data()