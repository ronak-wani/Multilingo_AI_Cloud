

import nest_asyncio
from starlette.responses import FileResponse
import os
import google.generativeai as genai
nest_asyncio.apply()
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()


class InputModel(BaseModel):
    question: str
    language: str
app = FastAPI(
    title="Chatbot API",
    version="1.0",
    description="Chatbot API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def root():
    return FileResponse('index.html')


@app.post("/api")

async def root(input: InputModel):
    language = input.language
    question = input.question
    os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
        ]
    )

    response = chat_session.send_message(f"Generate the answer to the {question} asked only in the following {language}")

    print(response.text)
    return {"text": response.text}

if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8010)