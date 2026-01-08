import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import numpy as np
import pandas as pd

keyword = st.session_state.get("keyword", "Apple")


st.title(f"{keyword} Brand Reputation")

st.markdown("<br>",unsafe_allow_html=True)
st.subheader("Keywords")

STOPWORDS = {
    "the","a","an","and","or","but","if","in","on","at","to","for","of","is","are",
    "was","were","it","this","that","these","those","i","you","he","she","they","via",
    "them","we","us","with","as","by","from","be","been","has","have","had","now",
    "not","so","do","does","did","can","could","would","should","will","just","its",
    "about","into","out","up","down","over","under","again","s","am","im","<url>","<user>"
}

fallback_text = (
    "Sample Text Empty DataFrame"
    "Brand Sentiment Analysis"
    "Social Pulse"
)

df = st.session_state.get("df", None)

if df is None or df.empty:
    text_data = fallback_text
else:
    text_col = "body" if "body" in df.columns else ("text" if "text" in df.columns else None)

    if text_col is None:
        text_data = fallback_text
    else:
        text_data = " ".join(df[text_col].astype(str).tolist())

words = text_data.lower().split()

words = [w for w in words if w not in STOPWORDS]

freq = dict(Counter(words).most_common(25))

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='#FDFDF8',
    colormap='Greens'
).generate_from_frequencies(freq)

fig_wc, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig_wc)


st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Top Tweets")
st.markdown("<br>", unsafe_allow_html=True)

df = st.session_state.get("df", pd.DataFrame())
fallback_positive = [
    "Sample Tweet as DataFrame is Empty",
    "Using Random Text as Input",
    "Can't Leave it Empty"
]
fallback_negative = [
    "Sample Tweet as DataFrame is Empty",
    "Using Random Text as Input",
    "Can't Leave it Empty"
]

def _render_card(text, comments=0, retweets=0, likes=0, positive=True):
    color = "green" if positive else "red"
    bg = "#F8FFF8" if positive else "#FFF6F6"
    footer = f""
    st.markdown(f"""
        <div style="
            border-left: 4px solid {color};
            padding: 10px 12px;
            margin-bottom: 10px;
            background-color: {bg};
            border-radius: 5px;
        ">{text}{footer}</div>
    """, unsafe_allow_html=True)

if df.empty:
    st.info("No dataset loaded — showing sample tweets.")
    st.markdown("<h4 style='margin-bottom:5px'>Positive Tweets</h4>", unsafe_allow_html=True)
    for t in fallback_positive:
        _render_card(t, positive=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-bottom:5px'>Negative Tweets</h4>", unsafe_allow_html=True)
    for t in fallback_negative:
        _render_card(t, positive=False)
else:
    text_col = "body" if "body" in df.columns else ("text" if "text" in df.columns else None)
    required = { "sentiment", "comment_num", "retweet_num", "like_num" }
    missing = [c for c in required if c not in df.columns]
    if text_col is None:
        missing.append("body/text")

    if missing:
        st.warning(f"Dataset missing columns: {', '.join(missing)} — showing sample tweets.")
        for t in fallback_positive:
            _render_card(t, positive=True)
        st.markdown("<br>", unsafe_allow_html=True)
        for t in fallback_negative:
            _render_card(t, positive=False)
    else:
        df_local = df.copy()
        for col in ["comment_num", "retweet_num", "like_num"]:
            df_local[col] = pd.to_numeric(df_local[col], errors="coerce").fillna(0).astype(int)
        df_local["engagement"] = df_local["comment_num"] + df_local["retweet_num"] + df_local["like_num"]
        def sentiment_label(val):
            if pd.isna(val):
                return "neutral"
            if isinstance(val, (int, float, np.number)):
                if val > 0: return "positive"
                if val < 0: return "negative"
                return "neutral"
            s = str(val).strip().lower()
            if "pos" in s: return "positive"
            if "neg" in s: return "negative"
            try:
                num = float(s)
                if num > 0: return "positive"
                if num < 0: return "negative"
            except:
                pass
            return "neutral"

        df_local["sent_label"] = df_local["sentiment"].apply(sentiment_label)

        positives = df_local[df_local["sent_label"] == "positive"].nlargest(3, "engagement")
        negatives = df_local[df_local["sent_label"] == "negative"].nlargest(3, "engagement")

        if positives.empty:
            st.info("No positive tweets in the selected data.")
        else:
            st.markdown("<h4 style='margin-bottom:5px'>Positive Tweets</h4>", unsafe_allow_html=True)
            for _, r in positives.iterrows():
                _render_card(r[text_col], comments=r["comment_num"], retweets=r["retweet_num"], likes=r["like_num"], positive=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if negatives.empty:
            st.info("No negative tweets in the selected data.")
        else:
            st.markdown("<h4 style='margin-bottom:5px'>Negative Tweets</h4>", unsafe_allow_html=True)
            for _, r in negatives.iterrows():
                _render_card(r[text_col], comments=r["comment_num"], retweets=r["retweet_num"], likes=r["like_num"], positive=False)
