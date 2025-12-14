from fastapi import FastAPI, UploadFile, File, Body, Form 
from typing import List
from pydantic import BaseModel
from pathlib import Path
from typing import List, Tuple, Optional
from jinja2 import Environment, FileSystemLoader
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from transformers import pipeline
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def retrieve_articles(company:str, role:str):

    gnews_api_key = "04d48be4ea74ddf64f4b4401f3fb8177"
    gnews_url = "https://gnews.io/api/v4/search"

    start_date_str = (datetime.now() - relativedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")

    # establish request session
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    seen_articles = []

    # create company query (can be modified for testing other ways to retrieve articles)
    company_query = f'{company} AND (earnings OR results OR revenue OR profit OR acquisition OR merger OR investment OR partnership OR strategy OR forecast OR guidance)'

    # format gnews request
    params = {
        "q": company_query,
        "lang": "en",
        "country": "us",
        "max": 25,
        "from": start_date_str,
        "apikey": gnews_api_key,
        "sortby": "publishedAt"
    }

    # make gnews request
    response = session.get(gnews_url, params=params, timeout=30)
    response.raise_for_status()
    gnews_data = response.json()

    articles = gnews_data.get("articles",[])
    parsed_articles = []

    for article in articles:
        if len(parsed_articles) >= 10:
            break
        title = article.get('title')
        link = article.get('url')
        content = article.get('content')[:1000]
        published = article.get('publishedAt')
        if not link or title in seen_articles:
            continue

        seen_articles.append(title)

        company_lower = company.lower()

        title_lower = (title or "").lower()
        content_lower = (article.get("content") or "").lower()

        if company_lower not in title_lower and company_lower not in content_lower:
            continue
        parsed_articles.append({
            'Title': title,
            'Link': link,
            'Published': published,
            'Full_Text': content,
        })    

    return parsed_articles

def summarize_articles(selected_articles: List[dict], company: str, role: str):
    summarizer = pipeline("text2text-generation", model="google/flan-t5-base")

    # summarize articles
    summaries = []
    prompts = []
    links = []
    titles = []

    for article in selected_articles:
        text = article.get('Full_Text').strip()

        if not text:
            summaries.append((article.get('Link'), article.get('Title'), 'Summary failure.'))
            continue

        prompt = f"Write a one sentence summary of the content contained in the following article; specifically highlight its impact or relevance on {company} in a context that would be useful for a job interview of a position as a {role} at the company:\n{text}"
        prompts.append(prompt)
        links.append(article.get('Link'))
        titles.append(article.get('Title'))

    for i in range(0, len(prompts), 10):
        # batch 10 prompts at a time
        batch_prompts = prompts[i:i+10]
        batch_links = links[i:i+10]
        batch_titles = titles[i:i+10]

        summary_results = summarizer(batch_prompts, truncation=True, do_sample=False)

        for link, title, summary_result in zip(batch_links, batch_titles, summary_results):
            summaries.append({'Link': link, 'Title': title, 'Summary': summary_result.get('generated_text').split('.')[0]})

    return summaries