import re

def parse_resume(resume_text: str):
    # Very naive parser – in production you’d use NLP or libraries like pyresparser
    name = re.findall(r"([A-Z][a-z]+ [A-Z][a-z]+)", resume_text)
    skills = re.findall(r"(Python|Java|SQL|TensorFlow|AWS)", resume_text)
    return {"name": name[0] if name else "Candidate", "skills": list(set(skills))}

def generate_messages(resume_info, role, company, channel, people, job):
    templates = {
        "linkedin_note": "Hi {person}, I came across {company} and I'm excited about opportunities there related to {job}. With my background in {skills}, I’d love to connect and learn more.",
        "cold_email": "Hi {person}, I’m reaching out regarding {job} roles at {company}. I bring experience in {skills} and I’d love to explore how I might contribute.",
        "linkedin_message": "Hi {person}, I’m reaching out regarding {job} roles at {company}. I bring experience in {skills} and I’d love to explore how I might contribute.",
    
    }
    skill_str = ", ".join(resume_info["skills"]) if resume_info["skills"] else "software development"
    results = {}
    for person in people:
        for i in channel:
            results.setdefault(i, [])
            msg = templates[i].format(
                person=person, company=company, skills=skill_str, job=job
            )
            results[i].append(msg)
    return results

def retrieve_and_summarize_articles(company, role):
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