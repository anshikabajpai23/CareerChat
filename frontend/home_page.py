import time
import streamlit as st
from ..backend.retrieve_articles import retrieve_and_summarize_articles

def home_page():
    st.set_page_config(page_title="News Article Retrieval & Summary", layout="centered")

    st.title("News Article Retrieval & Summary")

    # instructions
    st.markdown(
    """
**Instructions**

Click the button below to retrieve relevant news articles for the company and role you are applying for. Summaries will be generated for each article.

Then, check the box next to each article you would like to reference in your generated message.
"""
)

    # top controls (checkbox + button)
    col1, col2 = st.columns([1, 1])

    with col1:
        retrieve_btn = st.button("Retrieve News Articles", use_container_width=True)

    # placeholder for scrollable box
    box_placeholder = st.empty()

    # retrieval function - replace with backend function
    # def retrieve_and_summarize_articles(n=10):
    #     time.sleep(1)  # simulate network / processing time
    #     return [
    #         f"placeholder summary for article {i+1}"
    #         for i in range(n)
    #     ]

    # initialize session state
    if "articles" not in st.session_state:
        st.session_state.articles = None

    # when user clicks the button
    if retrieve_btn:

        # retrieve articles
        with st.spinner("Retrieving news articles..."):
            articles = retrieve_and_summarize_articles(10)

        st.session_state.articles = articles

    # render scrollable list of article summaries + checkboxes
    if st.session_state.articles is not None:
        articles = st.session_state.articles

        # build HTML for scrollable box with 10 unchecked checkboxes
        items_html = ""
        for i, summary in enumerate(articles, start=1):
            items_html += f"""
<div style="display:flex; align-items:flex-start; margin-bottom:0.75rem;">
    <input type="checkbox" id="article_{i}" style="margin-right:0.5rem;">
    <label for="article_{i}">
        <strong>Article {i}</strong> – {summary}
    </label>
    <br></br>
</div>
            """

        articles_html = f"""
<div style="
    border-radius: 8px;
    border: 1px solid #ddd;
    background-color: #f5f5f5;
    height: 320px;
    overflow-y: auto;
    padding: 0.75rem 1rem;
">
    {items_html}
</div>
        """

        box_placeholder.markdown(articles_html, unsafe_allow_html=True)