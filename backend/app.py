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

load_dotenv()
app = FastAPI()
templates_path =  "../templates"
env = Environment(loader=FileSystemLoader(templates_path))


class MessageRequest(BaseModel):
    role: str
    company: str
    message_type: str
    people: list[str]
    job: str
    history: list[str]
    resume_info: dict
    summaries: list[Tuple[str, str, str]]

@app.post("/generate-message/")
async def generate_messages( message_request: MessageRequest):
    print("Generating messages...")
    if message_request.message_type == 'LinkedIn connection notes':
        template = env.get_template("linkedin_msg.j2")
    elif message_request.message_type == 'Cover Letters':
        template = env.get_template("cover_letter.j2")

    print(message_request.json())
    results = {}
    for person in message_request.people:
        
        prompt = template.render(payload=message_request.resume_info,role=message_request.role, history=message_request.history, 
        position=message_request.job, news=message_request.summaries, company_name=message_request.company, Recipient_name=person)
        print(prompt)
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.responses.create(
            model="gpt-4.1-mini", #"gpt-4o-mini",
            input=[{
                "role": "system",
                "content": "You are a helpful assistant that helps people draft {message_type} based on their background and the job description."
            }, {
                "role": "user",
                "content": prompt
            }],
            max_output_tokens=512,
            temperature=0.2
        )
        print(response)
        results[person] = response.output[0].content[0].text
    return results

@app.post("/retrieve_articles/")
async def retrieve_articles(data: dict):

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
    company = data.get("company", "")
    role = data.get("role", "")

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

        if not company in title:
            # skip over any articles that do not mention the company in the title
            continue
        parsed_articles.append({
            'Title': title,
            'Link': link,
            'Published': published,
            'Full_Text': content,
        })    

    return parsed_articles

@app.post("/summarize_articles/")
async def summarize_articles(data: dict):
    summarizer = pipeline("text2text-generation", model="google/flan-t5-base")

    selected_articles = data.get("selected_articles", [])
    company = data.get("company", "")
    role = data.get("role", "")

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

    return {'summaries': summaries}