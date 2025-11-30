import os, time
from openai import OpenAI
import json
from pathlib import Path
from time import sleep

# Ensure a file is attached to the vector store
def _ensure_file_in_vector_store(client, vector_store_id: str, pdf_path: str, timeout_s: int = 60) -> str:
    if not Path(pdf_path).is_file():
        raise FileNotFoundError(f"PDF not found at: {pdf_path}")

    # Check file is already attached
    listing = client.vector_stores.files.list(vector_store_id=vector_store_id)
    if listing.data:
        return listing.data[0].id

    # Upload and attach
    with open(pdf_path, "rb") as f:
        uploaded = client.files.create(file=f, purpose="assistants")
    client.vector_stores.files.create(vector_store_id=vector_store_id, file_id=uploaded.id)

    # Wait until present
    deadline = timeout_s
    while deadline > 0:
        listing = client.vector_stores.files.list(vector_store_id=vector_store_id)
        if listing.data:
            return listing.data[0].id
        sleep(1)
        deadline -= 1

    raise TimeoutError("File did not appear in vector store within timeout.")

def parse_resume(user_input: str, pdf_path: str):
    os.environ["OPENAI_API_KEY"] = user_input
    client = OpenAI()
    
    # Create vector store for resume info
    resume_vector_store = client.vector_stores.create(name="resume_store")
    
    with open(pdf_path, "rb") as f:
        file_obj = client.files.create(file=f, purpose="assistants")
    client.vector_stores.files.create(
        vector_store_id=resume_vector_store.id,
        file_id=file_obj.id
    )
    
    vector_store_files = client.vector_stores.files.list(vector_store_id=resume_vector_store.id)
    print(vector_store_files)

    # Set up an assistant using gpt-4.1-mini model and the resume vector store
    assistant = client.beta.assistants.create(
        name="recruiting assistant",
        model="gpt-4.1-mini",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [resume_vector_store.id]}},
    )
    
    # Get file ID
    file_id = _ensure_file_in_vector_store(client, resume_vector_store.id, pdf_path)

    # Create thread and prompt
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=(
            "Please use the attached resume to extract this information:\n"
            "- name\n- email\n- education (degree, field, institution, graduation_date if present)\n"
            "- skills (list)\n"
            "- work_experience (title, company, start_date, end_date, responsibilities list)\n\n"
            "Respond ONLY with a single valid JSON object. Only include information from the resume, don't include markdown, don't include prose."
        ),
        attachments=[{"file_id": file_id, "tools": [{"type": "file_search"}]}],
    )
    
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
    
    # Wait until complete
    while True:
        time.sleep(2)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status in ("completed", "failed", "cancelled", "expired"):
            break
    if run.status != "completed":
        raise RuntimeError(f"Run ended with status: {run.status}")

    # Get the latest message text
    msgs = client.beta.threads.messages.list(thread_id=thread.id)
    text = None
    for m in msgs.data:
        if m.role == "assistant":
            for part in m.content:
                if part.type == "text":
                    text = part.text.value.strip()
                    break
            if text:
                break

    # Parse JSON
    if text:
        try:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                start = text.find("{"); end = text.rfind("}") + 1
                return json.loads(text[start:end])
        except Exception:
            return {"raw": text}
    return {"error": "No assistant text found"}
