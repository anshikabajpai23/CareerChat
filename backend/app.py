from fastapi import FastAPI, UploadFile, File, Body, Form 
from typing import List
from pydantic import BaseModel
from pathlib import Path
from typing import List
import util

app = FastAPI()

class MessageRequest(BaseModel):
    role: str   # recruiter, manager, friend, ex-colleague
    company: str
    channel: str   # linkedin, cold_email, etc.
    people: List[str]

@app.post("/generate-message/")
async def generate_message(
    file: UploadFile,
    role: str = Form(...),
    company: str = Form(...),
    channel: List[str] = Form(...),
    people: List[str] = Form(...),
    job: str = Form(...)
):
    resume_text = await file.read()
    resume_info = util.parse_resume(resume_text.decode("utf-8", errors="ignore"))
    messages = util.generate_messages(resume_info, role, company, channel, people, job)
    return {"messages": messages}