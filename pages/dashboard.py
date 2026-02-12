import streamlit as st

from connection.database import get_engine
from components.get_data import get_dates, get_stock_info_4_selected_date, get_biz_info_4_selected_ticker, get_stock_price_4_selected_date, get_stock_price_4_selected_date_n_symbol, get_relevant_news_4_selected_date_n_symbol
from components.visualization import metric_visualization, company_info_visualization, sentiment_and_ratings_visualization, price_volume_visualization, relevant_news_visualization
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configure the default settings of the page.
st.set_page_config(
    page_title="JINGHAO's Data Engineering Project",
    page_icon=":material/code_blocks:",
)

# Connect to the database and get dates
ENGINE = get_engine()


st.title("Stock Analysis Dashboard")
st.markdown('This dashboard provides insights for the top 3 most active stocks based on trading volume for a selected date.')
# Getting data

## Date selection
@st.cache_data
def load_dates():
    return get_dates(ENGINE)

## Getting the stock info from table mart_price_news__analysis for the selected date, and display the top 3 most active stocks based on volume
@st.cache_data
def load_selected_date_stock_info(selected_date):
    return get_stock_info_4_selected_date(ENGINE, selected_date)

## Getting the stock price, volume change data from mart_price_vol_chgn table for the selected date of the top 3 most active stocks, and display the charts
@st.cache_data
def load_selected_date_stock_price_info(selected_date):
    return get_stock_price_4_selected_date(ENGINE, selected_date)


# Main content
dates = load_dates()
if not dates:
    st.warning("No dates available. Please check the database connection.")
    st.stop()

selected_date = st.selectbox(label="Select a date", options=dates)
st.badge(label=f"Selected date: {selected_date}",
            icon=":material/today:",
            color="green")
st.session_state['selected_date'] = selected_date


## Create tabs for the top 3 most active stocks
df_selected_date_stock_info = load_selected_date_stock_info(selected_date=st.session_state['selected_date'])
df_stock_ranked_by_volume = df_selected_date_stock_info[['ticker', 'volume']].sort_values(by='volume', ascending=False).reset_index(drop=True)
list_most_active_stocks = df_stock_ranked_by_volume['ticker'][:3].tolist()

## Display data for the selected date
first_stock, second_stock, third_stock = st.tabs([f":1st_place_medal: {list_most_active_stocks[0]}", f":2nd_place_medal: {list_most_active_stocks[1]}", f":3rd_place_medal: {list_most_active_stocks[2]}"])
with first_stock:
    st.subheader(f"Stock Info for {list_most_active_stocks[0]} on {st.session_state['selected_date']}")
    df_first_stock_info = df_selected_date_stock_info[df_selected_date_stock_info['ticker'] == list_most_active_stocks[0]]
    
    # Display the company info. in a expander
    biz_info_first = get_biz_info_4_selected_ticker(ENGINE, list_most_active_stocks[0])
    company_info_visualization(biz_info_first, df_first_stock_info)

    # Display news sentiment and analystic ratings in pie charts
    sentiment_and_ratings_visualization(dataframe = df_first_stock_info, biz_info=biz_info_first, key=f'first_stock_{list_most_active_stocks[0]}')

    # Display the metrics
    metric_visualization(df_first_stock_info)

    # Display the price and volume charts
    df_price_vol = get_stock_price_4_selected_date_n_symbol(ENGINE, st.session_state['selected_date'], list_most_active_stocks[0])
    df_price_vol_chgn = load_selected_date_stock_price_info(selected_date=st.session_state['selected_date'])
    
    # Chart: Stock Price and Volume Movement (Past 100 Days)
    price_volume_visualization(df_price_vol, df_price_vol_chgn, df_first_stock_info, key=f'first_stock_{list_most_active_stocks[0]}')
    
    # Display relevant news articles
    df_first_stock_relevant_news = get_relevant_news_4_selected_date_n_symbol(
        ENGINE, st.session_state['selected_date'], list_most_active_stocks[0]
    )
    relevant_news_visualization(df_first_stock_relevant_news)
with second_stock:
    st.subheader(f"Stock Info for {list_most_active_stocks[1]} on {st.session_state['selected_date']}")
    df_second_stock_info = df_selected_date_stock_info[df_selected_date_stock_info['ticker'] == list_most_active_stocks[1]]
    
    # Display the company info. in a expander
    biz_info_second = get_biz_info_4_selected_ticker(ENGINE, list_most_active_stocks[1])
    company_info_visualization(biz_info_second, df_second_stock_info)
    
    # Display news sentiment and analystic ratings in pie charts
    sentiment_and_ratings_visualization(dataframe = df_second_stock_info, biz_info=biz_info_second, key=f'second_stock_{list_most_active_stocks[1]}')
    
    # Display the metrics
    metric_visualization(df_second_stock_info)

    # Display the price and volume charts
    df_price_vol = get_stock_price_4_selected_date_n_symbol(ENGINE, st.session_state['selected_date'], list_most_active_stocks[1])
    df_price_vol_chgn = load_selected_date_stock_price_info(selected_date=st.session_state['selected_date'])
    
    # Chart: Stock Price and Volume Movement (Past 100 Days)
    price_volume_visualization(df_price_vol, df_price_vol_chgn, df_second_stock_info, key=f'second_stock_{list_most_active_stocks[1]}')
    
    # Display relevant news articles
    df_second_stock_relevant_news = get_relevant_news_4_selected_date_n_symbol(
        ENGINE, st.session_state['selected_date'], list_most_active_stocks[1]
    )
    relevant_news_visualization(df_second_stock_relevant_news)

with third_stock:
    st.subheader(f"Stock Info for {list_most_active_stocks[2]} on {st.session_state['selected_date']}")

    # Get data for the third most active stock
    df_third_stock_info = df_selected_date_stock_info[df_selected_date_stock_info['ticker'] == list_most_active_stocks[2]]
    biz_info_third = get_biz_info_4_selected_ticker(ENGINE, list_most_active_stocks[2])
    
    # Display the company info. in a expander
    company_info_visualization(biz_info_third, df_third_stock_info)
    
    # Display news sentiment and analystic ratings in pie charts
    sentiment_and_ratings_visualization(dataframe = df_third_stock_info, biz_info=biz_info_third, key=f'third_stock_{list_most_active_stocks[2]}')
    
    # Display the metrics
    metric_visualization(df_third_stock_info)

    # Display the price and volume charts
    df_price_vol = get_stock_price_4_selected_date_n_symbol(ENGINE, st.session_state['selected_date'], list_most_active_stocks[2])
    df_price_vol_chgn = load_selected_date_stock_price_info(selected_date=st.session_state['selected_date'])
    
    ## Chart: Stock Price and Volume Movement (Past 100 Days)
    price_volume_visualization(df_price_vol, df_price_vol_chgn, df_third_stock_info, key=f'third_stock_{list_most_active_stocks[2]}')

    # Display relevant news articles
    df_third_stock_relevant_news = get_relevant_news_4_selected_date_n_symbol(
        ENGINE, st.session_state['selected_date'], list_most_active_stocks[2]
    )
    relevant_news_visualization(df_third_stock_relevant_news)

#-------------------------------------------------------------------
# Footer - diclaimer
st.markdown("---")
st.markdown("""
<div style="font-family: sans-serif; font-size: 0.9em; color: gray; text-align: center;">
  <p>Disclaimer: The data presented in this dashboard is for educational and illustrative purposes only. It should not be construed as financial advice or a recommendation to buy or sell any securities. Always conduct your own research and consult with a qualified financial advisor before making investment decisions.</p>
</div>
""", unsafe_allow_html=True,
    text_alignment='left')

#-------------------------------------------------------------------
st.markdown("© 2026 JINGHAO CHEN. All rights reserved.")
# End of the page