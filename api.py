from fastapi import FastAPI
from pydantic import BaseModel
from model import get_answer
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Query(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Legal AI API running"}

@app.post("/ask")
def ask_question(query: Query):
    answer = get_answer(query.question)
    return {"answer": answer}