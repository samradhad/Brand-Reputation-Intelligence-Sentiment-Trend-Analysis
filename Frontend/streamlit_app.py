import streamlit as st
import pandas as pd
import os
import datetime
import subprocess
import sys
from pathlib import Path
from cards import widgets_card

keyword = st.session_state.get("keyword", "Apple")
time_period = st.session_state.get("time_period", "Last 7 Days")
start_date = st.session_state.get("start_date", datetime.datetime.today().date() - pd.Timedelta(days=7))
end_date = st.session_state.get("end_date", datetime.datetime.today().date())

data_path = f"./Processed_Datasets/{keyword}_processed.csv"
known_keywords = ["Apple", "Amazon", "Google", "Tesla", "Microsoft"]

if keyword in known_keywords and os.path.exists(data_path):
    df = pd.read_csv(data_path)
    if df.empty:
        st.warning(f"Dataset for {keyword} exists but is empty.")
    else:
        print(f"Dataset for {keyword} loaded successfully. Rows: {len(df)}")
else:
    def process_custom_keyword(keyword):
        processed_path = Path(f"./Processed_Datasets/{keyword}_processed.csv")
        raw_path = Path(f"./Dataset/{keyword}.csv")
        launched_key = f"launched_{keyword}"

        if processed_path.exists():
            return
        if not raw_path.exists():
            return
        if not st.session_state.get(launched_key, False):
            cmd = [sys.executable, "./Frontend/processor.py", "--keyword", keyword]
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            st.session_state[launched_key] = True
    process_custom_keyword(keyword)
    df = pd.DataFrame(columns=["post_date", "body", "comment_num", "retweet_num", "like_num", "sentiment"])

    if Path(f"./Processed_Datasets/{keyword}_processed.csv").exists():
        df = pd.read_csv(f"./Processed_Datasets/{keyword}_processed.csv")
    else:
        if Path(f"./Dataset/{keyword}.csv").exists():
            st.info(f"No processed dataset found for `{keyword}`. Background processing has been started.")
            if st.button("Check / Load processed dataset"):
                if Path(f"./Processed_Datasets/{keyword}_processed.csv").exists():
                    df = pd.read_csv(f"./Processed_Datasets/{keyword}_processed.csv")
                    st.session_state["df"] = df
                    st.experimental_rerun()
                else:
                    st.warning("Still processing — please try again in a few seconds.")
        else:
            st.info(f"No local dataset found for {keyword}, using empty DataFrame.")


if not df.empty:
    df["post_date"] = pd.to_datetime(df["post_date"], errors="coerce")
    df = df.dropna(subset=["post_date"])

    if isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date):
        df_filtered = df[(df["post_date"].dt.date >= start_date) & (df["post_date"].dt.date <= end_date)]
    else:
        today = pd.Timestamp.today().date()
        df_filtered = df[(df["post_date"].dt.date >= today - pd.Timedelta(days=7)) & (df["post_date"].dt.date <= today)]
else:
    df_filtered = df

delta_net_sentiment = 0
delta_likes = 0
delta_retweets = 0
delta_comments = 0
delta_mentions = 0
delta_positive_pct = 0

if not df_filtered.empty:
    period_days = (end_date - start_date).days + 1 if start_date and end_date else 7
    prev_start = start_date - pd.Timedelta(days=period_days) if start_date else (pd.Timestamp.today().date() - pd.Timedelta(days=period_days*2))
    prev_end = start_date - pd.Timedelta(days=1) if start_date else (pd.Timestamp.today().date() - pd.Timedelta(days=period_days))

    df_prev = df[(df["post_date"].dt.date >= prev_start) & (df["post_date"].dt.date <= prev_end)]

    if not df_prev.empty:
        pos_prev = (df_prev["sentiment"] == "positive").mean()
        neg_prev = (df_prev["sentiment"] == "negative").mean()
        net_sentiment_prev = round(pos_prev - neg_prev, 3)
        avg_likes_prev = int(df_prev["like_num"].mean()) if not df_prev["like_num"].isna().all() else 0
        avg_retweets_prev = int(df_prev["retweet_num"].mean()) if not df_prev["retweet_num"].isna().all() else 0
        avg_comments_prev = int(df_prev["comment_num"].mean()) if not df_prev["comment_num"].isna().all() else 0
        total_mentions_prev = len(df_prev)
    else:
        net_sentiment_prev = avg_likes_prev = avg_retweets_prev = avg_comments_prev = total_mentions_prev = 0

    sentiment_counts = df_filtered["sentiment"].value_counts(normalize=True).to_dict()
    sentiment_percentages = {
        "Positive": round(sentiment_counts.get("positive", 0) * 100, 2),
        "Neutral": round(sentiment_counts.get("neutral", 0) * 100, 2),
        "Negative": round(sentiment_counts.get("negative", 0) * 100, 2),
    }

    avg_likes = int(df_filtered["like_num"].mean()) if not df_filtered["like_num"].isna().all() else 0
    avg_retweets = int(df_filtered["retweet_num"].mean()) if not df_filtered["retweet_num"].isna().all() else 0
    avg_comments = int(df_filtered["comment_num"].mean()) if not df_filtered["comment_num"].isna().all() else 0
    total_mentions = len(df_filtered)
    pos = sentiment_counts.get("positive", 0)
    neg = sentiment_counts.get("negative", 0)
    net_sentiment = round(pos - neg, 3)

    daily_sentiment = (
        df_filtered.groupby(df_filtered["post_date"].dt.date)["sentiment"]
        .apply(lambda x: (x == "positive").mean() - (x == "negative").mean())
        .reset_index(name="net_sentiment")
    )

    daily_volume = (
        df_filtered.groupby(df_filtered["post_date"].dt.date)
        .size()
        .reset_index(name="tweet_volume")
    )

    delta_net_sentiment = round(net_sentiment - net_sentiment_prev, 3)
    delta_likes = avg_likes - avg_likes_prev
    delta_retweets = avg_retweets - avg_retweets_prev
    delta_comments = avg_comments - avg_comments_prev
    delta_mentions = total_mentions - total_mentions_prev

    positive_curr_pct = sentiment_percentages["Positive"]
    if not df_prev.empty:
        positive_prev_pct = round((df_prev["sentiment"] == "positive").mean() * 100, 2)
    else:
        positive_prev_pct = 0
    delta_positive_pct = round(positive_curr_pct - positive_prev_pct, 2)

else:
    sentiment_percentages = {"Positive": 0, "Neutral": 0, "Negative": 0}
    avg_likes = avg_retweets = avg_comments = total_mentions = net_sentiment = 0
    daily_sentiment = pd.DataFrame(columns=["post_date", "net_sentiment"])
    daily_volume = pd.DataFrame(columns=["post_date", "tweet_volume"])

st.session_state.df = df_filtered
st.session_state.sentiment_percentages = sentiment_percentages
st.session_state.avg_likes = avg_likes
st.session_state.avg_retweets = avg_retweets
st.session_state.avg_comments = avg_comments
st.session_state.total_mentions = total_mentions
st.session_state.net_sentiment = net_sentiment
st.session_state.daily_sentiment = daily_sentiment
st.session_state.daily_volume = daily_volume
st.session_state.delta_net_sentiment = delta_net_sentiment
st.session_state.delta_likes = delta_likes
st.session_state.delta_retweets = delta_retweets
st.session_state.delta_comments = delta_comments
st.session_state.delta_mentions = delta_mentions
st.session_state.delta_positive_pct = delta_positive_pct

pages = [
    st.Page("home.py", title="Home", icon=":material/home:"),
    st.Page("Trends.py", title="Trends", icon=":material/trending_up:"),
    st.Page("Insights.py", title="Insights", icon=":material/insert_chart:"),
]

st.markdown(
    """
    <style>
        [data-testid="stSidebarNavItems"]::before {
            content: "Social Pulse";
            display: block;
            text-align: center;
            margin-top: 0px;
            margin-bottom: 20px;
            font-size: 20px;
            font-weight: 800;
            color: #31333F;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

page = st.navigation(pages)
page.run()

with st.sidebar.container(height=240):
    widgets_card()
