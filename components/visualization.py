import math
import streamlit as st
import plotly.express as px
import plotly.express as px
import plotly.graph_objects as go

def metric_visualization(dataframe):
    # Helpers to coalesce NaN/None to sensible defaults
    def safe_float(val, default=0.0):
        try:
            f = float(val)
            return 0.0 if math.isnan(f) else f
        except Exception:
            return default

    def safe_int(val, default=0):
        try:
            i = int(val)
            return default if math.isnan(i) else i
        except Exception:
            return default

    with st.container(border=True,
                        horizontal_alignment="center",
                        vertical_alignment="center"):
        #-------------------------------------------------------------------
        # Closing Price and Average Price (Past 100 Days)
        close_price_col, avg_price_col = st.columns(2)
        close_price_col.metric(
            label="Closing Price",
            value=f"${safe_float(dataframe['price'].values[0]):,.2f}",
            delta=safe_float(dataframe['change_percentage'].values[0]) / 100,
            format="percent",
        )
        # close_price_change_amount.metric(
        #     label="Change Amount",
        #     value=f"${safe_float(dataframe['change_amount'].values[0]):,.2f}"
        # )

        avg_price_col.metric(
            label="Average price (Past 100 Days)",
            value=f"${safe_float(dataframe['avg_close_price_past_100days'].values[0]):,.2f}",
            delta="Above Current Price" if dataframe['price_vs_100days_avg'].values[0] == 'Below Average 100 Days price' else "Below Current Price",
            delta_arrow="off",
            delta_color="green" if dataframe['price_vs_100days_avg'].values[0] == 'Above Average 100 Days price' else "red"
        )
        
        #-------------------------------------------------------------------
        # Volume and Average Volume (Past 100 Days)
        volume_col, avg_volume_col = st.columns(2)
        volume_col.metric(
            label="Volume",
            value=f"{safe_int(dataframe['volume'].values[0]):,}"
            
        )

        avg_volume_col.metric(
            label="Average volume (Past 100 Days)",
            value=f"{safe_int(dataframe['avg_volume_past_100days'].values[0]):,}",
            delta="Below Current Volume" if dataframe['volume_vs_100days_avg'].values[0] == 'Above Average 100 Days volume' else "Above Current Volume",
            delta_arrow="off",
            delta_color="green" if dataframe['volume_vs_100days_avg'].values[0] == 'Above Average 100 Days volume' else "red"
        )

        # #-------------------------------------------------------------------
        # # Recent relevant news sentiment analysis
        # st.caption("Recent Relevant News Sentiment Analysis:")
        # try:
        #     bullish, neutral, bearish, avg_sentiment_score = st.columns(4)
        #     bullish.metric(
        #         label="Bullish",
        #         value=f"{safe_int(dataframe['bullish_count'].values[0])}",
        #     )
        #     neutral.metric(
        #         label="Neutral",
        #         value=f"{safe_int(dataframe['neutral_count'].values[0])}",
        #     )
        #     bearish.metric(
        #         label="Bearish",
        #         value=f"{safe_int(dataframe['bearish_count'].values[0])}",
        #     )
        #     avg_sentiment_score.metric(
        #         label="Average Sentiment Score",
        #         value=f"{safe_float(dataframe['avg_sentiment_score'].values[0]):.2f}",
        #     )
        # except TypeError as e:
        #     st.error("No news data available for this stock on the selected date.")
        #     pass

#-------------------------------------------------------------------
# Company Info visualization
def company_info_visualization(biz_info, selected_df):
    try:
    # Guard against empty datasets to avoid index errors
        if (biz_info is None or biz_info.empty) or (selected_df is None or selected_df.empty):
            st.warning("Company info not available for this ticker. It may be a ETF without underlying company data.")
            pass
        else:
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
                    industry.metric(label="Industry", value=biz_info['Industry'].values[0], width='content')
                    
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
    except Exception:
        pass
#-------------------------------------------------------------------
# News Sentiment and Analyst Ratings visualization
def sentiment_and_ratings_visualization(dataframe, biz_info, key):
    with st.expander("News Sentiment and Analyst Ratings"):
        with st.container():
            news_sentiment_cols, analyst_rating_cols = st.columns(2)
            with news_sentiment_cols:
                sentiment_labels = {
                    'bullish_count': 'Bullish',
                    'neutral_count': 'Neutral',
                    'bearish_count': 'Bearish',
                    'somewhat_bullish_count': 'Somewhat Bullish',
                    'somewhat_bearish_count': 'Somewhat Bearish',
                }
                df_news_sentiment = (
                    dataframe[['bullish_count', 'neutral_count', 'bearish_count', 'somewhat_bullish_count', 'somewhat_bearish_count']]
                    .melt(var_name='sentiment', value_name='count')
                    .replace({'sentiment': sentiment_labels})
                )

                # Check if there is any data to render
                if df_news_sentiment.empty or df_news_sentiment['count'].sum() == 0:
                    st.warning("News sentiment data not available.")
                else:
                    fig_news_sentiment = px.pie(df_news_sentiment, 
                                                names='sentiment', 
                                                values='count', 
                                                title='News Sentiment Distribution')
                    fig_news_sentiment.update_layout(
                                                    legend=dict(
                                                        orientation="h",
                                                        yanchor="top",
                                                        y=-0.2,
                                                        xanchor="center",
                                                        x=0.5
                                                    ),
                                                    title=dict(x=0.5, xanchor="center")
                                                )
                    try:
                        st.plotly_chart(fig_news_sentiment, theme="streamlit", width='stretch', key=f"{key}_news")
                    except Exception as e:
                        st.warning(f"Unable to render news sentiment chart: {e}")
            with analyst_rating_cols:
                rating_labels = {
                    'AnalystRatingStrongBuy': 'Strong Buy',
                    'AnalystRatingBuy': 'Buy',
                    'AnalystRatingHold': 'Hold',
                    'AnalystRatingSell': 'Sell',
                    'AnalystRatingStrongSell': 'Strong Sell',
                }
                df_biz_analyst_rating = (
                    biz_info[['AnalystRatingStrongBuy', 'AnalystRatingBuy', 'AnalystRatingHold', 'AnalystRatingSell', 'AnalystRatingStrongSell']]
                    .melt(var_name='rating', value_name='count')
                    .replace({'rating': rating_labels})
                )

                # Check if there is any data to render
                if df_biz_analyst_rating.empty or df_biz_analyst_rating['count'].sum() == 0:
                    st.warning("Analyst ratings data not available.")
                else:
                    fig_analyst_rating = px.pie(df_biz_analyst_rating, 
                                                names='rating', 
                                                values='count', 
                                                title='Analyst Ratings Distribution')
                    fig_analyst_rating.update_layout(
                                                    legend=dict(
                                                        orientation="h",
                                                        yanchor="top",
                                                        y=-0.2,
                                                        xanchor="center",
                                                        x=0.5
                                                    ),
                                                    title=dict(x=0.5, xanchor="center")
                                                )
                    try:
                        st.plotly_chart(fig_analyst_rating, theme="streamlit", width='stretch', key=f"{key}_analyst")
                    except Exception as e:
                        st.warning(f"Unable to render analyst rating chart: {e}")


#-------------------------------------------------------------------
# Price and Volume visualization
def price_volume_visualization(df_price_vol, df_price_vol_chgn, df_stock_info, key):
    import math

    def safe_float(val):
        try:
            f = float(val)
            return None if math.isnan(f) else f
        except Exception:
            return None

    if df_price_vol is None or df_price_vol.empty:
        st.info("No price/volume data available.")
        return
    if df_stock_info is None or df_stock_info.empty:
        st.info("No price statistics available.")
        return

    avg_price = safe_float(df_stock_info["avg_close_price_past_100days"].values[0])
    max_price = safe_float(df_stock_info["max_price_past_100days"].values[0])
    min_price = safe_float(df_stock_info["min_price_past_100days"].values[0])

    layout = dict(
        hoversubplots="axis",
        title=dict(text="Stock Price and Volume Movement (Past 100 Days)", x=0.5, xanchor="center"),
        hovermode="x unified",
        grid=dict(rows=2, columns=1),
    )

    data = [
        go.Candlestick(
            x=df_price_vol["price_date"],
            open=df_price_vol["open_price"],
            high=df_price_vol["high_price"],
            low=df_price_vol["low_price"],
            close=df_price_vol["close_price"],
            name="Price",
            xaxis="x",
            yaxis="y"
        ),
        go.Bar(
            x=df_price_vol["price_date"],
            y=df_price_vol["volume"],
            name="Volume",
            xaxis="x",
            yaxis="y2"
        ),
    ]
    if avg_price is not None:
        data.append(
            go.Scatter(
                x=df_price_vol["price_date"],
                y=[avg_price] * len(df_price_vol),
                mode="lines",
                name="Avg Close (100d)",
                line=dict(color="blue", dash="dash"),
                xaxis="x",
                yaxis="y"
            )
        )
    if max_price is not None:
        data.append(
            go.Scatter(
                x=df_price_vol["price_date"],
                y=[max_price] * len(df_price_vol),
                mode="lines",
                name="Max Price (100d)",
                line=dict(color="red", dash="dot"),
                xaxis="x",
                yaxis="y"
            )
        )
    if min_price is not None:
        data.append(
            go.Scatter(
                x=df_price_vol["price_date"],
                y=[min_price] * len(df_price_vol),
                mode="lines",
                name="Min Price (100d)",
                line=dict(color="green", dash="dot"),
                xaxis="x",
                yaxis="y"
            )
        )

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
    )
    st.plotly_chart(fig, theme="streamlit", width='stretch', key=f"{key}_price_volume_movement")

    # Chart: Stock Price and Volume Changes (Past 100 Days)
    layout = dict(
        hoversubplots="axis",
        title=dict(text="Stock Price and Volume Changes (Past 100 Days)", x=0.5, xanchor="center"),
        hovermode="x unified",
        grid=dict(rows=2, columns=1),
    )

    data = [
        go.Scatter(
            x=df_price_vol_chgn["price_date"],
            y=df_price_vol_chgn["pct_daily_change"],
            xaxis="x",
            yaxis="y",
            name="% Daily Change of Stock Price"
        ),
        go.Scatter(
            x=df_price_vol_chgn["price_date"],
            y=df_price_vol_chgn["diff_vol"],
            xaxis="x",
            yaxis="y2",
            name="Daily Change of Volume"
        ),
    ]

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )

    st.plotly_chart(fig, theme="streamlit", width='stretch', key=f"{key}_price_volume_changes")

#-------------------------------------------------------------------
# Relevant news articles visualization
def relevant_news_visualization(df_relevant_news):
    with st.container(border=True):
        st.subheader("Relevant News Articles")
        if df_relevant_news is not None and not df_relevant_news.empty:
            for _, row in df_relevant_news.iterrows():
                sentiment_icon = ":ox:" if row['ticker_sentiment_label'] == 'Bullish' else ":bear:" if row['ticker_sentiment_label'] == 'Bearish' else ":neutral_face:"
                st.markdown(f"{sentiment_icon} [{row['title']}]({row['url']})")
        else:
            st.info("No news articles available for this stock on the selected date.")