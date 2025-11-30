import os, time
from openai import OpenAI
import json

def parse_resume(user_input: str, pdf_path: str):
    os.environ["OPENAI_API_KEY"] = user_input
    client = OpenAI()
    
    # #Create vector store for resume information.
    # resume_vector_store = client.vector_stores.create(
    #     name="resume_store"
    # )
    
    # file_obj = client.files.create(
    #     file=open(pdf_path, "rb"),
    #     purpose="assistants"
    # )
    
    # client.vector_stores.files.create(
    #     vector_store_id=resume_vector_store.id,
    #     file_id=file_obj.id
    # )
    
    # vector_store_files = client.vector_stores.files.list(
    #   vector_store_id=resume_vector_store.id
    # )
    # print(vector_store_files)
    
    # #Set up an assistant using gpt-4.1-mini and the resume's vector stor
    # assistant = client.beta.assistants.create(
    #     name="recruiting assistant",
    #     model="gpt-4.1-mini",
    #     tools=[{"type": "file_search"}],
    #     tool_resources={
    #         "file_search": { "vector_store_ids": [resume_vector_store.id] }
    #     }
    # )
    
    # #Get file id for our resume vector store
    # file_id = client.vector_stores.files.list(vector_store_id=resume_vector_store.id).data[0].id
    
    # #Create thread and prompt for resume json
    # thread = client.beta.threads.create()
    # client.beta.threads.messages.create(
    #     thread_id=thread.id,
    #     role="user",
    #     content=(
    #         "Please use the attached resume to extract this information:\n"
    #         "- name\n- email\n- education (degree, field, institution, graduation_date if present)\n"
    #         "- skills (list)\n"
    #         "- work_experience (title, company, start_date, end_date, responsibilities list)\n\n"
    #         "Respond ONLY with a single valid JSON object. Only include information from the resume, don't include markdown, don't include prose."
    #     ),
    #     attachments=[
    #         {
    #             "file_id": file_id,
    #             "tools": [{"type": "file_search"}]
    #         }
    #     ],
    # )
    
    # run = client.beta.threads.runs.create(
    #     thread_id=thread.id,
    #     assistant_id=assistant.id,
    # )
    
    # # We need to make sure it completes before the next step (we got errors otherwise)
    # while run.status != "completed":
    #     time.sleep(5)
    #     run = client.beta.threads.runs.retrieve(
    #         thread_id=thread.id,
    #         run_id=run.id
    #     )
    
    # msgs = client.beta.threads.messages.list(thread_id=thread.id)
    # text = None
    # for m in msgs.data:
    #     if m.role == "assistant":
    #         for part in m.content:
    #             if part.type == "text":
    #                 text = part.text.value.strip()
    
    # #Formatting json
    # start = text.find("{"); end = text.rfind("}") + 1
    # json_str = text[start:end]
    # data = json.loads(json_str)
    
    # #Printing json
    # print(json.dumps(data, indent=2, ensure_ascii=False))
    
    # #Save json to file called payload.json
    # with open("payload.json", "w", encoding="utf-8") as f:
    #     json.dump(data, f, indent=2, ensure_ascii=False)
