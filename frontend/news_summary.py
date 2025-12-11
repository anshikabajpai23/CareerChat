import streamlit as st
import requests


def news_summary():
    st.set_page_config(page_title="News Article Retrieval & Summary", layout="centered")

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

    # when user clicks the button
    if retrieve_btn:

        # retrieve articles
        with st.spinner("Retrieving news articles..."):
            data = {"company": 'Microsoft', "role": 'Software Engineer'}
            response = requests.post("http://127.0.0.1:8000/retrieve_articles/").json()

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
            

            st.session_state.summaries = [
                article for i, article in enumerate(articles, start=1)
                if st.session_state.get(f"article_{i}", False)
            ]

            print(f"Selected articles: {st.session_state.summaries}")

#     print("News summary page")
#     st.session_state.company = st.text_input("Company name", key='company_input')
#     st.session_state.summaries=[
#     ('https://www.foxnews.com/tech/windows-10-users-face-ransomware-nightmare-microsoft-support-ends-2025-worldwide', 'Windows 10 Users Face Ransomware Nightmare - Microsoft Support Ends 2025 Worldwide', 'Microsoft warns that over 90% of ransomware attacks target unsupported Windows 10 systems, urging users to upgrade ahead of support ending worldwide in 2025.')
#     , ('https://www.cnbc.com/2025/11/01/meta-alphabet-amazon-microsoft-earnings-ads.html', 'While AI spending is top of mind, online ads are driving a lot of Big Tech’s growth', 'Microsoft (alongside Meta, Alphabet and Amazon) reported ad- and cloud-driven earnings, reinforcing its expanding role in AI/ads environments.')
#     , ('https://www.cnbc.com/2025/10/31/tech-ai-google-meta-amazon-microsoft-spend.html', 'Tech’s $380 billion splurge: This quarter’s winners and losers of the AI spending boom', 'Microsoft signalled a continuing ramp-up in AI infrastructure investment, matching peers in increasing data center and AI-capex spending.')
#     , ('https://finance.yahoo.com/news/jim-cramer-says-microsoft-reported-134117610.html', 'Title 4', 'Cramer commented that although Microsoft delivered a strong quarter, its stock was still hit partly because of investor concern over its aggressive investment pace.')
#     , ('https://www.testingcatalog.com/microsoft-to-broaden-copilot-portraits-with-new-use-cases/', 'Title 5', 'Microsoft is expanding its Copilot Portraits feature (AI-avatar tool) into new use cases like public speaking and job-prep modelling.')
#     , ('https://www.forbes.com/sites/daveywinder/2025/11/01/new-warning-as-microsoft-windows-attacks-confirmed---no-fix-available/', 'Title 6', 'Microsoft acknowledged ongoing attacks exploiting a Windows vulnerability (CVE-2025-9491) with no fix yet available, raising urgent security concerns.')
#     , ('https://timesofindia.indiatimes.com/technology/tech-news/100000-tech-layoffs-in-2025-amazon-microsoft-intel-and-these-companies-cut-thousands-of-jobs/articleshow/125015287.cms', 'Title 7', 'Microsoft is among major tech firms cutting thousands of jobs (9,000 reportedly) in 2025 amid restructuring and shifting toward AI-driven operations.')
# ]