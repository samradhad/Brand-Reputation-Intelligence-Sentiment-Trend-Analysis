import streamlit as st
import plotly.express as px
import pandas as pd

st.title(f"{st.session_state.get('keyword')} Brand Reputation")

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Sentiment Over Time")

daily_sentiment = st.session_state.get("daily_sentiment", pd.DataFrame(columns=["post_date", "net_sentiment"]))
if not daily_sentiment.empty:
    fig_line = px.line(
        daily_sentiment,
        x="post_date",
        y="net_sentiment",
        labels={"post_date": "Date", "net_sentiment": "Sentiment Score"},
        color_discrete_sequence=["#059669"]
    )
    fig_line.update_yaxes(range=[-1, 1])
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.info("No sentiment data available for the selected period.")

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Tweet Volume Over Time")

daily_volume = st.session_state.get("daily_volume", pd.DataFrame(columns=["post_date", "tweet_volume"]))
if not daily_volume.empty:
    fig_bar = px.bar(
        daily_volume,
        x="post_date",
        y="tweet_volume",
        labels={"post_date": "Date", "tweet_volume": "Tweet Volume"},
        color_discrete_sequence=["#059669"]
    )
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("No tweet volume data available for the selected period.")
