import streamlit as st
import requests


def home_page():
    resume = st.file_uploader("Upload your resume", type=["pdf", "txt"], key='uploader')
    print(resume)
