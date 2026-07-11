import streamlit as st

from connection.database import get_engine
from components.get_data import get_dates, get_stock_info_4_selected_date, get_biz_info_4_selected_ticker, get_stock_price_4_selected_date, get_stock_price_4_selected_date_n_symbol, get_relevant_news_4_selected_date_n_symbol
from components.visualization import metric_visualization, company_info_visualization, sentiment_and_ratings_visualization, price_volume_visualization, relevant_news_visualization


# Configure the default settings of the page.
st.set_page_config(
    page_title="JINGHAO's Data Engineering Project",
    page_icon=":material/code_blocks:",
)

st.title("Tickers Analysis Dashboard",text_alignment='center')
st.markdown('The top 3 most active tickers based on trading volume for a selected date.',text_alignment='center')
# st.markdown('''[Tableau Version](https://public.tableau.com/views/TickersAnalysisDashboard/Dashboard?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)''', text_alignment='right')
# st.page_link("https://public.tableau.com/views/TickersAnalysisDashboard/Dashboard?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link", label="Tableau Version")
# st.page_link("https://github.com/chenjinghao/ms_fabric_project", label="Microsoft Fabric & Power BI Version")
# Getting data

# Connect to the database
@st.cache_resource
def load_engine():
    return get_engine()

try:
    ENGINE = load_engine()
except Exception as exc:
    st.error("Database connection is not configured correctly.")
    st.caption(str(exc))
    st.stop()

## Date selection
@st.cache_data
def load_dates(_engine):
    return get_dates(_engine)

## Getting the ticker info from table mart_price_news__analysis for the selected date, and display the top 3 most active tickers based on volume
@st.cache_data
def load_selected_date_stock_info(selected_date):
    return get_stock_info_4_selected_date(ENGINE, selected_date)

## Getting the ticker price, volume change data from mart_price_vol_chgn table for the selected date of the top 3 most active tickers, and display the charts
@st.cache_data
def load_selected_date_stock_price_info(selected_date):
    return get_stock_price_4_selected_date(ENGINE, selected_date)


# Main content
try:
    dates = load_dates(ENGINE)
except Exception as exc:
    st.error("Unable to load available dates from the database.")
    st.caption(str(exc))
    st.stop()

if not dates:
    st.warning(
        "Connected to the database, but no dates were found in mart_price_news__analysis. "
        "Run the backend ELT pipeline or load data into this table."
    )
    st.stop()

selected_date = st.selectbox(label="Select a date", options=dates)
st.badge(label=f"Selected date: {selected_date}",
            icon=":material/today:",
            color="green")
st.session_state['selected_date'] = selected_date


## Create tabs for the top 3 most active stocks
try:
    df_selected_date_stock_info = load_selected_date_stock_info(selected_date=st.session_state['selected_date'])
except Exception as exc:
    st.error("Unable to load ticker data for the selected date.")
    st.caption(str(exc))
    st.stop()

if df_selected_date_stock_info is None or df_selected_date_stock_info.empty:
    st.warning(f"No ticker data found for {st.session_state['selected_date']}.")
    st.stop()

df_stock_ranked_by_volume = df_selected_date_stock_info[['ticker', 'volume']].sort_values(by='volume', ascending=False).reset_index(drop=True)
list_most_active_stocks = df_stock_ranked_by_volume['ticker'][:3].tolist()

## Display data for the selected date
first_stock, second_stock, third_stock = st.tabs([f":1st_place_medal: {list_most_active_stocks[0]}", f":2nd_place_medal: {list_most_active_stocks[1]}", f":3rd_place_medal: {list_most_active_stocks[2]}"])
with first_stock:
    st.subheader(f"Tickers Info for {list_most_active_stocks[0]} on {st.session_state['selected_date']}")
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
    
    # Chart: Tickers Price and Volume Movement (Past 100 Days)
    price_volume_visualization(df_price_vol, df_price_vol_chgn, df_first_stock_info, key=f'first_stock_{list_most_active_stocks[0]}')
    
    # Display relevant news articles
    df_first_stock_relevant_news = get_relevant_news_4_selected_date_n_symbol(
        ENGINE, st.session_state['selected_date'], list_most_active_stocks[0]
    )
    relevant_news_visualization(df_first_stock_relevant_news)
with second_stock:
    st.subheader(f"Tickers Info for {list_most_active_stocks[1]} on {st.session_state['selected_date']}")
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
    
    # Chart: Tickers Price and Volume Movement (Past 100 Days)
    price_volume_visualization(df_price_vol, df_price_vol_chgn, df_second_stock_info, key=f'second_stock_{list_most_active_stocks[1]}')
    
    # Display relevant news articles
    df_second_stock_relevant_news = get_relevant_news_4_selected_date_n_symbol(
        ENGINE, st.session_state['selected_date'], list_most_active_stocks[1]
    )
    relevant_news_visualization(df_second_stock_relevant_news)

with third_stock:
    st.subheader(f"Tickers Info for {list_most_active_stocks[2]} on {st.session_state['selected_date']}")

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
    
    ## Chart: Tickers Price and Volume Movement (Past 100 Days)
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
