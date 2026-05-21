import sqlalchemy
import pandas as pd

def _read_sql(engine, query, params=None):
    if engine is None:
        raise RuntimeError("Database engine was not created.")

    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(query), params or {})
        return pd.DataFrame(result.fetchall(), columns=result.keys())

# Function to get distinct dates from the database
def get_dates(engine):
    query = "SELECT DISTINCT date FROM mart_price_news__analysis ORDER BY date DESC"

    df = _read_sql(engine, query)
    return df["date"].tolist()

# Function to get stock info for a selected date
def get_stock_info_4_selected_date(engine, selected_date):
    query = """
        SELECT *
        FROM mart_price_news__analysis
        WHERE date = :selected_date
        ORDER BY volume DESC
    """
    return _read_sql(engine, query, {"selected_date": selected_date})


def get_biz_info_4_selected_ticker(engine, selected_ticker):
    query = 'SELECT * FROM biz_info_lookup WHERE "Symbol" = :selected_ticker'
    return _read_sql(engine, query, {"selected_ticker": selected_ticker})

def get_stock_price_4_selected_date(engine, selected_date):
    query = "SELECT * FROM mart_price_vol_chgn WHERE extraction_date = :selected_date"
    return _read_sql(engine, query, {"selected_date": selected_date})

#-------------------------------------------------------------------
def get_stock_price_4_selected_date_n_symbol(engine, selected_date, selected_symbol):
    query = """
        SELECT *
        FROM stg_price
        WHERE extraction_date = :selected_date
          AND symbol = :selected_symbol
    """
    return _read_sql(
        engine,
        query,
        {"selected_date": selected_date, "selected_symbol": selected_symbol},
    )

#-------------------------------------------------------------------
def get_relevant_news_4_selected_date_n_symbol(engine, selected_date, selected_symbol):
    query = """
        SELECT url, title, time_published_date, ticker_sentiment_label
        FROM mart_news__recent
        WHERE extraction_date = :selected_date
          AND mentioned_ticker = :selected_symbol
        ORDER BY time_published_date DESC
    """
    return _read_sql(
        engine,
        query,
        {"selected_date": selected_date, "selected_symbol": selected_symbol},
    )
