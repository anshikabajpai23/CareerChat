import json
import os
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv 

import openai

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

openai.api_key = OPENAI_KEY

with open("/Users/anshikabajpai/Desktop/nlp/project/CareerChat/payload.json","r", encoding="utf-8") as f:
    payload = json.load(f)

role = 'recruiter'
history = ['indiana university', 'society of women engineers conference 2025']
position = 'machine learning engineer'

news = [
    ('https://www.foxnews.com/tech/windows-10-users-face-ransomware-nightmare-microsoft-support-ends-2025-worldwide', 'Microsoft warns that over 90% of ransomware attacks target unsupported Windows 10 systems, urging users to upgrade ahead of support ending worldwide in 2025.')
    , ('https://www.cnbc.com/2025/11/01/meta-alphabet-amazon-microsoft-earnings-ads.html', 'Microsoft (alongside Meta, Alphabet and Amazon) reported ad- and cloud-driven earnings, reinforcing its expanding role in AI/ads environments.')
    , ('https://www.cnbc.com/2025/10/31/tech-ai-google-meta-amazon-microsoft-spend.html', 'Microsoft signalled a continuing ramp-up in AI infrastructure investment, matching peers in increasing data center and AI-capex spending.')
    , ('https://finance.yahoo.com/news/jim-cramer-says-microsoft-reported-134117610.html', 'Cramer commented that although Microsoft delivered a strong quarter, its stock was still hit partly because of investor concern over its aggressive investment pace.')
    , ('https://www.testingcatalog.com/microsoft-to-broaden-copilot-portraits-with-new-use-cases/', 'Microsoft is expanding its Copilot Portraits feature (AI-avatar tool) into new use cases like public speaking and job-prep modelling.')
    , ('https://www.forbes.com/sites/daveywinder/2025/11/01/new-warning-as-microsoft-windows-attacks-confirmed---no-fix-available/', 'Microsoft acknowledged ongoing attacks exploiting a Windows vulnerability (CVE-2025-9491) with no fix yet available, raising urgent security concerns.')
    , ('https://timesofindia.indiatimes.com/technology/tech-news/100000-tech-layoffs-in-2025-amazon-microsoft-intel-and-these-companies-cut-thousands-of-jobs/articleshow/125015287.cms', 'Microsoft is among major tech firms cutting thousands of jobs (9,000 reportedly) in 2025 amid restructuring and shifting toward AI-driven operations.')
]


env = Environment(loader=FileSystemLoader('/Users/anshikabajpai/Desktop/nlp/project/CareerChat/src/prompt_templates'))
template=env.get_template("template.j2")

prompt = template.render(payload=payload,role=role, history=history, position=position, news=news, company_name="Microsoft", Recipient_name="Alex Johnson")
print(prompt)

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "system",
        "content": "You are a helpful assistant that helps people draft job application emails based on their background and the job description."
    }, {
        "role": "user",
        "content": prompt
    }],
    max_tokens=512,
    temperature=0.2
)
print(response)

reply = response['choices'][0]['message']['content']
print("Generated Email Draft:\n", reply)

