import streamlit as st

def metric_visualization(dataframe):
    with st.container(border=True,
                        horizontal_alignment="center",
                        vertical_alignment="center"):
        #-------------------------------------------------------------------
        # Closing Price and Average Price (Past 100 Days)
        close_price_col, close_price_change_amount, avg_price_col = st.columns(3)
        close_price_col.metric(
            label="Closing Price",
            value=f"${float(dataframe['price'].values[0]):,.2f}",
            delta=float(dataframe['change_percentage'].values[0]) / 100,
            format="percent",
        )
        close_price_change_amount.metric(
            label="Change Amount",
            value=f"${float(dataframe['change_amount'].values[0]):,.2f}"
        )

        avg_price_col.metric(
            label="Average price (Past 100 Days)",
            value=f"${float(dataframe['avg_close_price_past_100days'].values[0]):,.2f}",
            delta="Above Current Price" if dataframe['price_vs_100days_avg'].values[0] == 'Below Average 100 Days price' else "Below Current Price",
            delta_arrow="off",
            delta_color="green" if dataframe['price_vs_100days_avg'].values[0] == 'Above Average 100 Days price' else "red"
        )
        
        #-------------------------------------------------------------------
        # Volume and Average Volume (Past 100 Days)
        volume_col, avg_volume_col = st.columns(2)
        volume_col.metric(
            label="Volume",
            value=f"{int(dataframe['volume'].values[0]):,}"
            
        )

        avg_volume_col.metric(
            label="Average volume (Past 100 Days)",
            value=f"{int(dataframe['avg_volume_past_100days'].values[0]):,}",
            delta="Below Current Volume" if dataframe['volume_vs_100days_avg'].values[0] == 'Above Average 100 Days volume' else "Above Current Volume",
            delta_arrow="off",
            delta_color="green" if dataframe['volume_vs_100days_avg'].values[0] == 'Above Average 100 Days volume' else "red"
        )

        #-------------------------------------------------------------------
        # Recent relevant news sentiment analysis
        st.caption("Recent Relevant News Sentiment Analysis:")
        try:
            bullish, neutral, bearish, avg_sentiment_score = st.columns(4)
            bullish.metric(
                label="Bullish",
                value=f"{int(dataframe['bullish_count'].values[0])}",
            )
            neutral.metric(
                label="Neutral",
                value=f"{int(dataframe['neutral_count'].values[0])}",
            )
            bearish.metric(
                label="Bearish",
                value=f"{int(dataframe['bearish_count'].values[0])}",
            )
            avg_sentiment_score.metric(
                label="Average Sentiment Score",
                value=f"{float(dataframe['avg_sentiment_score'].values[0]):.2f}",
            )
        except TypeError as e:
            st.error("No news data available for this stock on the selected date.")
            pass

#-------------------------------------------------------------------
# Company Info visualization
def company_info_visualization(biz_info, selected_df):
    # Guard against empty datasets to avoid index errors
    if biz_info is None or biz_info.empty:
        st.warning("Company info not available for this ticker.")
        return
    if selected_df is None or selected_df.empty:
        st.warning("Price data not available for this ticker.")
        return

    current_price = selected_df['price'].values[0]
    with st.expander("Company Info"):
        with st.container():
            st.title(biz_info['Name'].values[0])
            st.caption(f"Listed on {biz_info['Exchange'].values[0]}")
            st.metric(label="Market Cap", value=f"${float(biz_info['MarketCapitalization'].values[0])/1e9:.2f} B")
            st.subheader("About the company")
            st.markdown(biz_info['Description'].values[0])
            st.link_button(
                label="Visit Official Website",
                url=biz_info['OfficialSite'].values[0],
                type="primary",
                width='content'
                )
            sector, industry = st.columns(2)
            sector.metric(label="Sector", value=biz_info['Sector'].values[0])
            industry.metric(label="Industry", value=biz_info['Industry'].values[0])
            
            # Market data
            st.write(f"Current price: {current_price}")
            wk52_high, wk52_low, day50_avg, day200_avg = st.columns(4)
            wk52_high.metric(label="52-Week High", 
                             value=f"${float(biz_info['52WeekHigh'].values[0]):.2f}")
            wk52_low.metric(label="52-Week Low", 
                            value=f"${float(biz_info['52WeekLow'].values[0]):.2f}")
            day50_avg.metric(label="50-Day Avg", 
                             value=f"${float(biz_info['50DayMovingAverage'].values[0]):.2f}")
            day200_avg.metric(label="200-Day Avg", 
                              value=f"${float(biz_info['200DayMovingAverage'].values[0]):.2f}")

            # Analyst ratings
            Strong_Buy, Buy, Hold, Sell, Strong_Sell = st.columns(5)
            Strong_Buy.metric(label="Strong Buy", value=biz_info['AnalystRatingStrongBuy'].values[0])
            Buy.metric(label="Buy", value=biz_info['AnalystRatingBuy'].values[0])
            Hold.metric(label="Hold", value=biz_info['AnalystRatingHold'].values[0])
            Sell.metric(label="Sell", value=biz_info['AnalystRatingSell'].values[0])
            Strong_Sell.metric(label="Strong Sell", value=biz_info['AnalystRatingStrongSell'].values[0])
