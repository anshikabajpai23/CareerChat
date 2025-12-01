import streamlit as st
import requests
import json
import os

def get_resume():
    # return st.session_state.get('uploaded_resume', None)
    # with open("payload.json","r", encoding="utf-8") as f:
    if os.path.exists("payload.json"):
        with open("payload.json","r", encoding="utf-8") as f:
            # payload = json.load(f)
            return json.load(f)
    return {"error": "payload.json not found"}

def message_generation_page():
    # resume = st.file_uploader("Upload your resume", type=["pdf", "txt"]) #remove
    resume_info = get_resume()
    role = st.selectbox("Who are you contacting?", ["recruiter", "manager", "friend", "ex-colleague", "senior", "director"], key = 'role_select')
    message_type = st.selectbox("Message type", ['LinkedIn connection notes', 'Cover Letters'], key='message_type_select')
    company = st.text_input("Company name", key='company_input')
    history = st.multiselect("Message type", ['LinkedIn connection notes', 'Cover Letters'], key='history_select')
    job = st.selectbox("Which Job role?", ["Software", "Machine Learning", "Data Science", "Game Development"], key='job_select')
    people = st.text_area("List of people (comma-separated)", key='text').split(",")
    if st.button("Generate Messages", key='button') and resume_info:
        # files = {"file": resume} #remove
        data = {"role": role, "company": company, "message_type": message_type, "people": people, "job": job, "history": history, "resume_info": resume_info} #add resume
        response = requests.post("http://127.0.0.1:8000/generate-message/", data=data)
        st.json(response.json())