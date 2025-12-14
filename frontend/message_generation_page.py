import streamlit as st
import requests
import json
from backend.message_generation import generate_messages
from backend.news_articles import summarize_articles
import os

def get_resume():
    if os.path.exists(st.session_state.uploads_dir / "payload.json"):
        with open(st.session_state.uploads_dir / "payload.json","r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "payload.json not found"}

def get_history(resume_info):
    history = []
    for i in range(len(resume_info["work_experience"])):
        history.append(resume_info["work_experience"][i]["company"])
    for i in range(len(resume_info["education"])):
        history.append(resume_info["education"][i]["institution"])
    return history

def message_generation_page():
    raw_summaries = summarize_articles(selected_articles=st.session_state.selected_articles, company=st.session_state.company_name, role=st.session_state.job_name)
    parsed_summaries = []
    print(raw_summaries)
    for summary in raw_summaries:

        parsed_summaries.append((summary.get('Link'), summary.get('Title'), summary.get('Summary')))
    st.session_state.summaries = parsed_summaries
    print("summaries: ", st.session_state.summaries)

    resume_info = get_resume()
    history = get_history(resume_info)
    role = st.selectbox("Who are you contacting?", ["recruiter", "manager", "friend", "ex-colleague", "senior", "director"], key = 'role_select')
    message_type = st.selectbox("Message type", ['LinkedIn connection notes', 'Cover Letters'], key='message_type_select')
    company=st.session_state.company_name
    history = st.multiselect("How do you know the person?", history, key='history_select')
    job = st.session_state.job_name
    people = st.text_area("List of people (comma-separated)", key='text').split(",")
    
    if st.button("Generate Messages", key='button') and resume_info:

        output = generate_messages(role=role, company=company, message_type=message_type, people=people, job=job, history=history, resume_info=resume_info, summaries=st.session_state.summaries)

        colors = ["#FFB6B9", "#B6E2D3", "#FFF2B2", "#B2D0FF"]  # light but readable
        text_color = "#111111"  # dark text for contrast in both light/dark modes

        for i, (key, value) in enumerate(output.items()):
            box_color = colors[i % len(colors)]
            
            st.markdown(
                f"""
                <div style="
                    background-color: {box_color};
                    color: {text_color};
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
                    width: 800px;
                ">
                    <strong>{key}</strong><br>
                    {value}
                </div>
                """,
                unsafe_allow_html=True
            )