import sqlalchemy
import pandas as pd

# Function to get distinct dates from the database
def get_dates(engine):
    query = "SELECT DISTINCT date FROM mart_price_news__analysis ORDER BY date DESC"

    try:
        with engine.connect() as conn:
            # 1. Execute using SQLAlchemy directly
            result = conn.execute(sqlalchemy.text(query))
            
            # 2. Construct DataFrame from the result object
            # result.fetchall() gets the data
            # result.keys() gets the column names
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

            # 3. put value from date column into a list
            date_list = df['date'].tolist()
            
            return date_list
    except Exception as e:
        print(e)

# Function to get stock info for a selected date
def get_stock_info_4_selected_date(engine, selected_date):
    query = f"SELECT * FROM mart_price_news__analysis WHERE date = '{selected_date}' ORDER BY volume DESC"

    try:
        with engine.connect() as conn:
            # 1. Execute using SQLAlchemy directly
            result = conn.execute(sqlalchemy.text(query))
            
            # 2. Construct DataFrame from the result object
            # result.fetchall() gets the data
            # result.keys() gets the column names
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            
            return df
    except Exception as e:
        print(e)        


def get_biz_info_4_selected_ticker(engine, selected_ticker):
    query = f"SELECT * FROM biz_info_lookup WHERE \"Symbol\" = '{selected_ticker}'"

    try:
        with engine.connect() as conn:
            # 1. Execute using SQLAlchemy directly
            result = conn.execute(sqlalchemy.text(query))
            
            # 2. Construct DataFrame from the result object
            # result.fetchall() gets the data
            # result.keys() gets the column names
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            
            return df
    except Exception as e:
        print(e)  