import streamlit as st
import requests


def news_summary():
    st.set_page_config(page_title="News Article Retrieval & Summary", layout="centered")

    # company and role inputs
    # if "company" not in st.session_state:
    #     st.session_state.company = ""
    # if "role" not in st.session_state:
    #     st.session_state.role = ""
    st.text_input("Company You Are Applying At:", key="company")
    st.text_input("Role You Are Applying For:", key="role")

    st.title("News Article Retrieval & Summary")

    # instructions
    st.markdown(
    """
**Instructions**

Click the button below to retrieve relevant news articles for the company and role you are applying for.

Then, check the box next to each article you would like to reference in your generated message.
"""
)

    # top controls
    col1, col2 = st.columns([1, 1])

    with col1:
        retrieve_btn = st.button("Retrieve News Articles", use_container_width=True)

    # placeholder for scrollable box
    box_placeholder = st.empty()

    # initialize session state
    if "articles" not in st.session_state:
        st.session_state.articles = None
    # persist previous selections; only set default if not present
    st.session_state.setdefault("selected_articles", [])

    # when user clicks the button
    if retrieve_btn:

        # retrieve articles
        with st.spinner("Retrieving news articles..."):
            data = {"company": st.session_state.company, "role": st.session_state.role}
            response = requests.post("http://127.0.0.1:8000/retrieve_articles/",json=data).json()

        st.session_state.articles = response

    # render scrollable list of article summaries + checkboxes
    if st.session_state.articles is not None:
        articles = st.session_state.articles

        for i in range(1, len(articles) + 1):
            # set default state to unchecked for each article
            st.session_state.setdefault(f"article_{i}", False)

        with st.expander("Retrieved Articles", expanded=True):

            # render Streamlit checkboxes inside expander
            for i, article in enumerate(articles, start=1):
                # add checkbox for each article - format of "Title - Summary" extracted from article object
                key=f"article_{i}"
                st.checkbox(f"**{article['Title']}** – {article['Link']}", key=key)
            

            st.session_state.selected_articles = [
                article for i, article in enumerate(articles, start=1)
                if st.session_state.get(f"article_{i}", False)
            ]

            # print(f"Selected articles: {st.session_state.selected_articles}")