import streamlit as st
import plotly.express as px
import pandas as pd


keyword = st.session_state.get("keyword", "Apple")
time_period = st.session_state.get("time_period", "Last 7 Days")

df = st.session_state.get("df", pd.DataFrame())
sentiment_percentages = st.session_state.get("sentiment_percentages", {"Positive": 0, "Neutral": 0, "Negative": 0})
avg_likes = st.session_state.get("avg_likes", 0)
avg_retweets = st.session_state.get("avg_retweets", 0)
avg_comments = st.session_state.get("avg_comments", 0)
total_mentions = st.session_state.get("total_mentions", 0)
net_sentiment = st.session_state.get("net_sentiment", 0)

delta_net_sentiment = st.session_state.get("delta_net_sentiment", 0)
delta_likes = st.session_state.get("delta_likes", 0)
delta_retweets = st.session_state.get("delta_retweets", 0)
delta_comments = st.session_state.get("delta_comments", 0)
delta_mentions = st.session_state.get("delta_mentions", 0)
delta_positive = st.session_state.get("delta_positive_pct", 0)

st.title(f"{keyword} Brand Reputation")

st.markdown("<br>",unsafe_allow_html=True)
st.subheader("Metrics")

cols = st.columns([10,1,10,1,10])
cols[0].metric(
    "Net Sentiment Score",
    f"{net_sentiment}",
    f"{delta_net_sentiment:+}",
    border=True
)
cols[2].metric(
    "Positive Sentiment",
    f"{sentiment_percentages['Positive']}%",
    f"{delta_positive:+}%",
    border=True
)
cols[4].metric(
    "Total mentions",
    f"{total_mentions}",
    f"{delta_mentions:+}",
    border=True
)

st.markdown("<br>",unsafe_allow_html=True)
cols = st.columns([10,1,10,1,10])

cols[0].metric(
    "Avg. Likes",
    f"{avg_likes}",
    f"{delta_likes:+}",
    border=True
)
cols[2].metric(
    "Avg. Retweets",
    f"{avg_retweets}",
    f"{delta_retweets:+}",
    border=True
)
cols[4].metric(
    "Avg. Replies",
    f"{avg_comments}",
    f"{delta_comments:+}",
    border=True
)

sentiment_data = {
    "Sentiment": ["Positive", "Neutral", "Negative"],
    "Percentage": [
        sentiment_percentages.get("Positive", 0),
        sentiment_percentages.get("Neutral", 0),
        sentiment_percentages.get("Negative", 0)
    ]
}
df1 = pd.DataFrame(sentiment_data)
fig = px.pie(
    df1,
    names="Sentiment",
    values="Percentage",
    color="Sentiment",
    color_discrete_map={"Positive": "green", "Neutral": "gray", "Negative": "red"},
    hole=0.3
)

fig.update_traces(textinfo="percent+label")

st.markdown("<br>",unsafe_allow_html=True)
st.subheader("Sentiment Distribution")
st.plotly_chart(fig, use_container_width=True)