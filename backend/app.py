from fastapi import FastAPI, UploadFile, File, Body, Form 
from typing import List
from pydantic import BaseModel
from pathlib import Path
from typing import List
import util
from jinja2 import Environment, FileSystemLoader
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
templates_path =  "../templates"
env = Environment(loader=FileSystemLoader(templates_path))
# openai.api_key = os.environ["OPENAI_API_KEY"]


class MessageRequest(BaseModel):
    role: str
    company: str
    message_type: str
    people: list[str]
    job: str
    history: list[str]
    resume_info: dict



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
        position=message_request.job, news=summaries, company_name=message_request.company, Recipient_name=person)
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


    #TODO: add news summary
summaries=[('https://www.pcgamer.com/games/sim/microsoft-flight-simulator-isnt-just-for-nerdy-dads-anymore-boeing-will-start-using-its-tech-to-train-actual-pilots/&ved=2ahUKEwjuosnx-OWQAxWaRDABHROfHFYQxfQBegQIARAC&usg=AOvVaw0Dpdv6zBkQXr0egyufnReV',
'The most recent incarnation of Microsoft\'s long-running flight simulator series is a genuine marvel, whether you fancy yourself an ace pilot or just want to crash spectacularly into the Eiffel Tower. Speaking more to the former instinct, Microsoft is teaming up with Boeing to put that high-fidelity simulation to work in a virtual training program for novice pilots. As noted in a press release from Boeing, the Virtual Airplane Procedures Trainer was announced last Thursday at the European Aviation Training Summit in Portugal. The release notes the new program is "powered by Microsoft Azure and Microsoft Flight Simulator," and is "designed to empower pilots and flight training teams with immersive, accessible and customizable tools that elevate pilot learning and readiness." It won\'t replace the physical flight simulators of yore but instead "reduce simulator familiarization time," as the release notes. It\'s also, to be clear, not Microsoft Flight Simulator—just a virtual trainer that uses the sim as a foundation in some capacity. There\'s a video showing off an overview of the trainer and its associated regimen on Boeing\'s website, and it seems primarily driven by a lesson plan that points prospective pilots'),
('https://www.tomshardware.com/software/windows/microsoft-announces-first-test-build-for-windows-11-26h1-aimed-at-nvidia-n1x-and-snapdragon-x2-first-h1-release-in-windows-11s-history-is-reserved-for-armpcs&ved=2ahUKEwjuosnx-OWQAxWaRDABHROfHFYQxfQBegQIBxAC&usg=AOvVaw2NJUiNBFEVrVX5UPZygjOj',
'Microsoft has just released the first build of Windows 11 26H1 — Preview Build 28000 — in the Canary channel of the Insider Preview program. 26H1 is in testing phases right now, and it will officially release early next year. This update is intended for a specific subset of users, with various reports suggesting that it is ARM. There are unsubstantiated rumors floating around, pointing to the upcoming Snapdragon X2 Elite and Nvidia N1X systems as candidates — since Qualcomm has scheduled the launch of its upcoming chips for early 2026, lining up with the 26H1 release. There are unsubstantiated rumors floating around, pointing to the upcoming Snapdragon X2 Elite and Nvidia N1X systems as candidates — since Qualcomm has scheduled the launch of its upcoming chips for early 2026, lining up with the 26H1 release. Despite the implication, Microsoft doesn\'t explicitly mention any names in its announcement, so this is all speculation. "26H1 is not a feature update for version 25H2 and only includes platform changes to support specific silicon. There is no action required from customers," says the Redmont'),
('https://inews.zoombangla.com/microsofts-new-ai-chip-aims-to-challenge-nvidias-market-dominance/&ved=2ahUKEwjuosnx-OWQAxWaRDABHROfHFYQxfQBegQIBhAC&usg=AOvVaw0Nyv6PZ9tBvVQg4TBmjD6S',
'Where to Watch Sunday Night Football: Steelers vs Chargers Live Guide The main keyword is “where to watch Sunday Night Football”. If you’re tuning in, you’ll want to know exactly how...'),
('https://simplywall.st/stocks/us/software/nasdaq-msft/microsoft/news/is-microsofts-valuation-justified-after-recent-ai-partnershi&ved=2ahUKEwjuosnx-OWQAxWaRDABHROfHFYQxfQBegQICBAC&usg=AOvVaw07F9nD6sQm2BNecTZ3as9F',
"Microsoft's stock has recently dipped 4.1% in the last week and 5.3% over the past month, hinting at shifting sentiment or new risks in play. When we distill it down to valuation, Microsoft scores 4 out of 6 on our valuation score, suggesting it is undervalued in more areas than not. We'll break down what that score really means using a range of valuation methods and, at the end, reveal a fresh perspective that can help you make even more confident decisions."),
('https://kalkinemedia.com/us/news/market-updates/sp-500-technology-leaders-apple-nvidia-and-microsoft-in-focus&ved=2ahUKEwj64M70-OWQAxVvTDABHXqbESUQxfQBegQIAxAC&usg=AOvVaw3yJhXuRvOBvrGUzgv6XU10',
'This article is based on a Microsoft blog post, which was originally published on the Microsoft blog at http://blog.microsoft.com/en-us/en-us-blog.html.'),
('https://kalkinemedia.com/us/stocks/technology/microsoft-shines-across-nyse-composite-index-with-steady-tech-sector-leadership&ved=2ahUKEwj64M70-OWQAxVvTDABHXqbESUQxfQBegQIBBAC&usg=AOvVaw2bb0qXG9d6MIkH1nvEQjZK',
'This article is based on a Microsoft blog post, which was originally published on the Microsoft blog at http://blog.microsoft.com/en-us/en-us-blog.html.'),
('https://ts2.tech/en/microsoft-stock-today-msft-eight%25E2%2580%2591day-slide-hits-longest-streak-since-2011-close-catalysts-and-whats-next-nov-7-2025/&ved=2ahUKEwj3mJX1-OWQAxWJTjABHWEkAKMQxfQBegQIAhAC&usg=AOvVaw2Z5qooL9eeGBrY0y54wLan',
'(NASDAQ: SPOT) has a market capitalization of $2.2 billion and a market capitalization of $2.2 billion as of the latest close (U.S. markets are closed on Sunday).'),
('https://finance.yahoo.com/video/trump-medias-q3-loss-microsoft-170918740.html&ved=2ahUKEwj3mJX1-OWQAxWJTjABHWEkAKMQxfQBegQIARAC&usg=AOvVaw2sozzSjd1Nh10x-YTFw1KE',
'US stocks falling today after Michigan Consumer sentiment came in below estimates and fell to a three-year low. Sweet Green is plunging after cutting its full-year outlook. Its third quarter results also disappointed as same-store sales fell by more than expected.'),
]