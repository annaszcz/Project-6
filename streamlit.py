import streamlit as st 
import pandas as pd 
from psycopg2 import sql
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Database connection parameters
load_dotenv()


# Function to get the connection to the database
def get_db_connection():
    #DATABASE_URL = os.getenv('DATABASE_URL')
    DATABASE_URL = st.secrets["DATABASE_URL"]
    engine = create_engine(DATABASE_URL)
    return engine

# Function to fetch bitcoin data from the database
def fetch_bitcoin_data(engine):
    query = "SELECT * FROM bitcoin_data_py ORDER BY date"
    df = pd.read_sql(query, engine)
    return df

# Function to fetch bitcoin news data from the database
def fetch_bitcoin_news(engine):
    query = "SELECT * FROM bitcoin_news_aws"
    df = pd.read_sql(query, engine)
    return df

# Get the database connection
conn = get_db_connection()

# Fetch the bitcoin data and news
bitcoin_data_df = fetch_bitcoin_data(conn)
bitcoin_news_df = fetch_bitcoin_news(conn)

# Display Bitcoin data
st.title("Bitcoin Data")
st.line_chart(bitcoin_data_df.set_index('date')['volume'])

# Display Bitcoin news
st.title("Bitcoin News")
st.write(bitcoin_news_df)

st.write(""" 
         # Test
         test
         """)