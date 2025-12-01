import pandas as pd
import streamlit as st
from home_page import home_page

from message_generation_page import message_generation_page
# st.title("Networking Message Generator")
print("Starting Streamlit app...")
print(f"Streamlit version: {st.user}")
st.title("CareerChat Home Page")

tab1, tab2, tab3 = st.tabs(["Profile Creation", "News summary", "Message Generation"])
with tab1:
    st.header("Profile Creation")
    # st.write("Welcome to the Message Generation tab!")
    home_page()


with tab3:
    st.header("Message Generation")
    st.write("Welcome to the Message Generation tab!")
    message_generation_page()


# if st.session_state.get("logged_in", False):
#     if st.button("Log in with Google", type="primary", icon=":material/login:"):
#         st.login()
# else:
#     st.html(f"Hello, <span style='color: orange; font-weight: bold;'></span>!")
#     st.write(home_page())

#     if st.button("Log out", type="secondary", icon=":material/logout:"):
#         st.logout()

# st.caption(f"Streamlit version {st.__version__}")