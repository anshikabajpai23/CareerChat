from pathlib import Path
from typing import List, Tuple, Optional
from jinja2 import Environment, FileSystemLoader
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
templates_path = Path(__file__).resolve().parent.parent / "templates"
env = Environment(loader=FileSystemLoader(str(templates_path)))

def generate_messages(role: str,
    company: str,
    message_type: str,
    people: list[str],
    job: str,
    history: list[str],
    resume_info: dict,
    summaries: list[Tuple[str, str, str]]):
    print("Generating messages...")
    if message_type == 'LinkedIn connection notes':
        template = env.get_template("linkedin_msg.j2")
    elif message_type == 'Cover Letters':
        template = env.get_template("cover_letter.j2")

    results = {}
    for person in people:
        
        prompt = template.render(payload=resume_info,role=role, history=history, 
        position=job, news=summaries, company_name=company, Recipient_name=person)
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
        results[person] = response.output[0].content[0].text
    return results