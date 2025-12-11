import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import requests
from home_page import home_page
from message_generation_page import message_generation_page
from news_summary import news_summary

if "tab_index" not in st.session_state:
    st.session_state.tab_index = 0

tabs = ["Profile Creation", "News Summary", "Message Generation"]

def next_tab():
    if st.session_state.tab_index == len(tabs) - 2:
        # trigger backend summarization call
        data = {"selected_articles": st.session_state.selected_articles, "company": st.session_state.company, "role": st.session_state.role}
        raw_summaries = requests.post("http://127.0.0.1:8000/summarize_articles/",json=data).json().get("summaries", [])
        parsed_summaries = []
        for summary in raw_summaries:
            parsed_summaries.append((summary.get('Link'), summary.get('Title'), summary.get('Summary')))
        st.session_state.summaries = parsed_summaries
        # print("summaries: ", st.session_state.summaries)
    if st.session_state.tab_index < len(tabs) - 1:
        st.session_state.tab_index += 1

def prev_tab():
    if st.session_state.tab_index > 0:
        st.session_state.tab_index -= 1

st.title("CareerChat Home Page")

current_tab = tabs[st.session_state.tab_index]

if current_tab == "Profile Creation":
    st.header("Profile Creation")
    home_page()
elif current_tab == "News Summary":
    st.header("News Summary")
    news_summary()
elif current_tab == "Message Generation":
    st.header("Message Generation")
    message_generation_page()

# Navigation buttons
col1, col2, col3 = st.columns([1,2,1])

with col1:
    st.button("PREVIOUS", on_click=prev_tab)

with col3:
    st.button("NEXT", on_click=next_tab)
