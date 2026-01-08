import streamlit as st
import datetime

def widgets_card():
    st.page_link("home.py", label="Search", icon=":material/search:")

    initial_keyword = st.session_state.get("keyword", "Apple")

    def _normalize_keyword():
        cur = st.session_state.get("keyword", "")
        if not isinstance(cur, str):
            return
        normalized = cur.strip().title()
        if normalized != cur:
            st.session_state["keyword"] = normalized

    _ = st.text_input("Enter Keyword", value=initial_keyword, key="keyword", on_change=_normalize_keyword)

    if "time_period" not in st.session_state:
        st.session_state.time_period = "Last 7 Days"

    period = st.selectbox(
        "Select Period",
        ["Last 7 Days", "Last 30 Days", "Custom"],
        index=["Last 7 Days", "Last 30 Days", "Custom"].index(st.session_state.time_period),
        key="time_period"
    )

    today = datetime.date.today()
    if period == "Last 7 Days":
        st.session_state.start_date = today - datetime.timedelta(days=7)
        st.session_state.end_date = today
    elif period == "Last 30 Days":
        st.session_state.start_date = today - datetime.timedelta(days=30)
        st.session_state.end_date = today
    elif period == "Custom":
        default_start = today - datetime.timedelta(days=7)
        default_end = today
        start_date, end_date = st.date_input("Select Range", value=(default_start, default_end))
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date

