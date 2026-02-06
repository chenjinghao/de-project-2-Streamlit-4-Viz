import streamlit as st

from connection.database import get_engine
from components.get_data import get_dates, get_stock_info_4_selected_date, get_biz_info_4_selected_ticker
from components.visualization import metric_visualization, company_info_visualization

# Configure the default settings of the page.
st.set_page_config(
    page_title="JINGHAO's Data Engineering Project",
    page_icon=":material/code_blocks:",
)

# Connect to the database and get dates
ENGINE = get_engine()


st.title("Stock Analysis Dashboard")
st.markdown('this is the about me page')

# Main content
## Date selection
@st.cache_data
def load_dates():
    return get_dates(ENGINE)

dates = load_dates()
selected_date = st.selectbox(label="Select a date", options=dates)
st.badge(label=f"Selected date: {selected_date}",
            icon=":material/today:",
            color="green")
st.session_state['selected_date'] = selected_date

## Display data for the selected date
@st.cache_data
def load_selected_date_stock_info(selected_date):
    return get_stock_info_4_selected_date(ENGINE, selected_date)

## Create tabs for the top 3 most active stocks
df_selected_date_stock_info = load_selected_date_stock_info(selected_date=st.session_state['selected_date'])
df_stock_ranked_by_volume = df_selected_date_stock_info[['ticker', 'volume']].sort_values(by='volume', ascending=False).reset_index(drop=True)

list_most_active_stocks = df_stock_ranked_by_volume['ticker'][:3].tolist()
first_stock, second_stock, third_stock = st.tabs([f":1st_place_medal: {list_most_active_stocks[0]}", f":2nd_place_medal: {list_most_active_stocks[1]}", f":3rd_place_medal: {list_most_active_stocks[2]}"])

with first_stock:
    st.subheader(f"Stock Info for {list_most_active_stocks[0]} on {st.session_state['selected_date']}")
    df_first_stock_info = df_selected_date_stock_info[df_selected_date_stock_info['ticker'] == list_most_active_stocks[0]]
    
    # Display the company info. in a expander
    biz_info = get_biz_info_4_selected_ticker(ENGINE, list_most_active_stocks[0])
    company_info_visualization(biz_info, df_first_stock_info)
    # Display the metrics
    metric_visualization(df_first_stock_info)


with second_stock:
    st.subheader(f"Stock Info for {list_most_active_stocks[1]} on {st.session_state['selected_date']}")
    df_second_stock_info = df_selected_date_stock_info[df_selected_date_stock_info['ticker'] == list_most_active_stocks[1]]
    
    # Display the company info. in a expander
    biz_info = get_biz_info_4_selected_ticker(ENGINE, list_most_active_stocks[1])
    company_info_visualization(biz_info, df_second_stock_info)
    
    # Display the metrics
    metric_visualization(df_second_stock_info)

with third_stock:
    st.subheader(f"Stock Info for {list_most_active_stocks[2]} on {st.session_state['selected_date']}")
    df_third_stock_info = df_selected_date_stock_info[df_selected_date_stock_info['ticker'] == list_most_active_stocks[2]]
    # Display the company info. in a expander
    biz_info = get_biz_info_4_selected_ticker(ENGINE, list_most_active_stocks[2])
    
    company_info_visualization(biz_info, df_third_stock_info)

    # Display the metrics
    metric_visualization(df_third_stock_info)

