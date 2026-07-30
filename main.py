from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import ask

# FastAPI application
app = FastAPI(
    title="AI Assistant",
    description="AI Assistant for handle company requests",
    version="1.0.0"

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

#Question format
class QuestionRequest(BaseModel):
    question: str

#Answer format
class AnswerResponse(BaseModel):
    question: str
    answer: str


@app.get("/")
def root():
    """Simple check API endpoint."""
    return {"status" : "OK", "message" : "Hello World" }

@app.post("/ask", response_model=AnswerResponse)
def ask(req: QuestionRequest):
    answer = ask(req.question)
    return AnswerResponse(question=req.question, answer=answer) 
    