import datetime
import os
import psycopg2
from dotenv import load_dotenv

def save_data(event, context):
    # Load the .env file
    load_dotenv()
    # Database connection parameters
    DATABASE_URL = os.getenv('url') 

    # Connect to the database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Create the table if it doesn't already exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS btcn_data (
            date DATE PRIMARY KEY,
            open NUMERIC,
            high NUMERIC,
            low NUMERIC,
            close NUMERIC,
            volume BIGINT
        )
    ''')
    conn.commit()  # Ensure the table creation is saved

    # fetch data from API (event in this case is test data)
    data = event   # This is just for testing the Lambda function from the Test Event JSON

    # Prepare lists for each column
    dates = []
    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []
    volumes = []

    # Extract data from the API response (JSON test event structure)
    for date_str in data["Time Series (Daily)"]:
        # Convert date_str to a datetime object
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        dates.append(date)
        open_prices.append(float(data["Time Series (Daily)"][date_str]['1. open']))
        high_prices.append(float(data["Time Series (Daily)"][date_str]['2. high']))
        low_prices.append(float(data["Time Series (Daily)"][date_str]['3. low']))
        close_prices.append(float(data["Time Series (Daily)"][date_str]['4. close']))
        volumes.append(int(data["Time Series (Daily)"][date_str]['5. volume']))

    # Insert each row into the table
    for date, open_price, high_price, low_price, close_price, vol in zip(dates, open_prices, high_prices, low_prices, close_prices, volumes):
        cur.execute('''
            INSERT INTO btcn_data (date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (date) DO NOTHING
        ''', (date, open_price, high_price, low_price, close_price, vol))

    # Commit the transactions and close the connection
    conn.commit()
    cur.close()
    conn.close()

    return "Data saved to Database successfully"
