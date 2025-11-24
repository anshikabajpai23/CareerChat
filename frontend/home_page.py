import streamlit as st
import requests
def home_page():
    resume = st.file_uploader("Upload your resume", type=["pdf", "txt"])
    role = st.selectbox("Who are you contacting?", ["recruiter", "manager", "friend", "ex-colleague", "senior", "director"])
    channel = st.multiselect("Message type", ["linkedin_message", "cold_email", "linkedin_note"])
    company = st.text_input("Company name")
    job = st.selectbox("Which Job role?", ["Software", "Machine Learning", "Data Science", "Game Development"])
    people = st.text_area("List of people (comma-separated)").split(",")
    if st.button("Generate Messages") and resume:
        files = {"file": resume}
        data = {"role": role, "company": company, "channel": channel, "people": people, "job": job}
        response = requests.post("http://127.0.0.1:8000/generate-message/", data=data, files=files)
        st.json(response.json())