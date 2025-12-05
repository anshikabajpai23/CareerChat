import time
import random
import requests
import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from newspaper import Article, Config
from GoogleNews import GoogleNews
from nltk.tokenize import sent_tokenize
from transformers import pipeline
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def retrieve_and_summarize_articles():
    return [
    ('https://www.foxnews.com/tech/windows-10-users-face-ransomware-nightmare-microsoft-support-ends-2025-worldwide', 'Microsoft warns that over 90% of ransomware attacks target unsupported Windows 10 systems, urging users to upgrade ahead of support ending worldwide in 2025.')
    , ('https://www.cnbc.com/2025/11/01/meta-alphabet-amazon-microsoft-earnings-ads.html', 'Microsoft (alongside Meta, Alphabet and Amazon) reported ad- and cloud-driven earnings, reinforcing its expanding role in AI/ads environments.')
    , ('https://www.cnbc.com/2025/10/31/tech-ai-google-meta-amazon-microsoft-spend.html', 'Microsoft signalled a continuing ramp-up in AI infrastructure investment, matching peers in increasing data center and AI-capex spending.')
    , ('https://finance.yahoo.com/news/jim-cramer-says-microsoft-reported-134117610.html', 'Cramer commented that although Microsoft delivered a strong quarter, its stock was still hit partly because of investor concern over its aggressive investment pace.')
    , ('https://www.testingcatalog.com/microsoft-to-broaden-copilot-portraits-with-new-use-cases/', 'Microsoft is expanding its Copilot Portraits feature (AI-avatar tool) into new use cases like public speaking and job-prep modelling.')
    , ('https://www.forbes.com/sites/daveywinder/2025/11/01/new-warning-as-microsoft-windows-attacks-confirmed---no-fix-available/', 'Microsoft acknowledged ongoing attacks exploiting a Windows vulnerability (CVE-2025-9491) with no fix yet available, raising urgent security concerns.')
    , ('https://timesofindia.indiatimes.com/technology/tech-news/100000-tech-layoffs-in-2025-amazon-microsoft-intel-and-these-companies-cut-thousands-of-jobs/articleshow/125015287.cms', 'Microsoft is among major tech firms cutting thousands of jobs (9,000 reportedly) in 2025 amid restructuring and shifting toward AI-driven operations.')
]