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
