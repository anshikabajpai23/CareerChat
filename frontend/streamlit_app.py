import pandas as pd
import streamlit as st
from news_page import home_page

st.title("Networking Message Generator")
print("Starting Streamlit app...")
print(f"Streamlit version: {st.user}")
if st.session_state.get("logged_in", False):
    if st.button("Log in with Google", type="primary", icon=":material/login:"):
        st.login()
else:
    st.html(f"Hello, <span style='color: orange; font-weight: bold;'></span>!")
    st.write(home_page())

    if st.button("Log out", type="secondary", icon=":material/logout:"):
        st.logout()

st.caption(f"Streamlit version {st.__version__}")