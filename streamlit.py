import streamlit as st 
import pandas as pd 
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

st.write ('Welcome')

# Database connection parameters 
load_dotenv()


# Function to get the connection to the database
def get_db_connection():
    DATABASE_URL = os.getenv('DATABASE_URL')
    # DATABASE_URL = st.secrets["DATABASE_URL"]
    engine = create_engine(DATABASE_URL)
    return engine

# Function to fetch bitcoin data from the database
def fetch_bitcoin_data(engine):
    query = "SELECT * FROM btcn_data ORDER BY date"
    df = pd.read_sql(query, engine)
    return df

# Function to fetch bitcoin news data from the database
def fetch_bitcoin_news(engine):
    query = "SELECT * FROM btcn_titles2"
    df = pd.read_sql(query, engine)
    return df

# Get the database connection
conn = get_db_connection()

# Fetch the bitcoin data and news
btcn_data = fetch_bitcoin_data(conn)
btcn_titles2 = fetch_bitcoin_news(conn)

# Display Bitcoin data
st.title("Bitcoin Data")
st.line_chart(btcn_data.set_index('date')['volume'])

# Display Bitcoin news
st.title("Bitcoin News")
st.write(btcn_titles2)

st.write(""" 
         # Test
         test
         """)