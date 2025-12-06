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



