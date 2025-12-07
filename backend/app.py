from fastapi import FastAPI, UploadFile, File, Body, Form 
from typing import List
from pydantic import BaseModel
from pathlib import Path
from typing import List, Tuple, Optional
from jinja2 import Environment, FileSystemLoader
from openai import OpenAI
from dotenv import load_dotenv
import os

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
async def retrieve_articles():
    # import time
    # import random
    # import requests
    # import pandas as pd
    # import nltk
    # nltk.download('punkt')
    # nltk.download('punkt_tab')
    # from datetime import datetime
    # from dateutil.relativedelta import relativedelta
    # from datetime import datetime
    # from dateutil.relativedelta import relativedelta
    # from newspaper import Article, Config
    # from GoogleNews import GoogleNews
    # from nltk.tokenize import sent_tokenize
    # from transformers import pipeline
    # from urllib3.util.retry import Retry
    # from requests.adapters import HTTPAdapter

    return [
    ('https://www.foxnews.com/tech/windows-10-users-face-ransomware-nightmare-microsoft-support-ends-2025-worldwide', 'Windows 10 Users Face Ransomware Nightmare - Microsoft Support Ends 2025 Worldwide', 'Microsoft warns that over 90% of ransomware attacks target unsupported Windows 10 systems, urging users to upgrade ahead of support ending worldwide in 2025.')
    , ('https://www.cnbc.com/2025/11/01/meta-alphabet-amazon-microsoft-earnings-ads.html', 'While AI spending is top of mind, online ads are driving a lot of Big Tech’s growth', 'Microsoft (alongside Meta, Alphabet and Amazon) reported ad- and cloud-driven earnings, reinforcing its expanding role in AI/ads environments.')
    , ('https://www.cnbc.com/2025/10/31/tech-ai-google-meta-amazon-microsoft-spend.html', 'Tech’s $380 billion splurge: This quarter’s winners and losers of the AI spending boom', 'Microsoft signalled a continuing ramp-up in AI infrastructure investment, matching peers in increasing data center and AI-capex spending.')
    , ('https://finance.yahoo.com/news/jim-cramer-says-microsoft-reported-134117610.html', 'Title 4', 'Cramer commented that although Microsoft delivered a strong quarter, its stock was still hit partly because of investor concern over its aggressive investment pace.')
    , ('https://www.testingcatalog.com/microsoft-to-broaden-copilot-portraits-with-new-use-cases/', 'Title 5', 'Microsoft is expanding its Copilot Portraits feature (AI-avatar tool) into new use cases like public speaking and job-prep modelling.')
    , ('https://www.forbes.com/sites/daveywinder/2025/11/01/new-warning-as-microsoft-windows-attacks-confirmed---no-fix-available/', 'Title 6', 'Microsoft acknowledged ongoing attacks exploiting a Windows vulnerability (CVE-2025-9491) with no fix yet available, raising urgent security concerns.')
    , ('https://timesofindia.indiatimes.com/technology/tech-news/100000-tech-layoffs-in-2025-amazon-microsoft-intel-and-these-companies-cut-thousands-of-jobs/articleshow/125015287.cms', 'Title 7', 'Microsoft is among major tech firms cutting thousands of jobs (9,000 reportedly) in 2025 amid restructuring and shifting toward AI-driven operations.')
]