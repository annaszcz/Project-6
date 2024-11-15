import datetime
# import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Database connection parameters
DATABASE_URL = os.getenv('url')
print(DATABASE_URL)

# Connect to the database
conn = psycopg2.connect(DATABASE_URL)

cur = conn.cursor()

print("connected")
def save_data(event, context):
    # fetch data from api
    # Parse the Data as JSON
    # data = event   #this is just to Test the lambda function from the Test Event Json
    data= event['responsePayload'] #this to get the returned data from the 1st lambda function 

    # Prepare lists for each column
    dates = []
    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []
    volumes = []

    # Extract data from the API response: {'2024-11-12': {'1. open': '7.6400', '2. high': '7.9900', '3. low': '7.5600', '4. close': '7.9600', '5. volume': '31154554'}
    for date_str in data["Time Series (Daily)"]:
        # Convert date_str to a datetime object
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        dates.append(date)
        open_prices.append(float(data["Time Series (Daily)"][date_str]['1. open']))
        high_prices.append(float(data["Time Series (Daily)"][date_str]['2. high']))
        low_prices.append(float(data["Time Series (Daily)"][date_str]['3. low']))
        close_prices.append(float(data["Time Series (Daily)"][date_str]['4. close']))
        volumes.append(int(data["Time Series (Daily)"][date_str]['5. volume']))

    # Convert lists into a DataFrame (optional, for verification or further processing)
    # df = pd.DataFrame({
    #    "date": dates,
    #   "open": open_prices,
    #    "high": high_prices,
    #    "low": low_prices,
    #    "close": close_prices,
    #    "volume": volumes
    # })

    # Insert each row individually to handle potential unique constraints
    for date, open_price, high_price, low_price, close_price, vol in zip(dates, open_prices, high_prices, low_prices, close_prices, volumes):
        cur.execute('''
            INSERT INTO btcn_data(date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (date) DO NOTHING
        ''', (date, open_price, high_price, low_price, close_price, vol))

    # Commit changes and close the cursor
    conn.commit()
    cur.close()
    
    return "Data saved to Database successfully"
