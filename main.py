from fastapi import FastAPI
from pydantic import BaseModel
from agent import ask_question

# FastAPI application
app = FastAPI(
    title="AI Assistant",
    description="AI Assistant for handle company requests",
    version="1.0.0"

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
    answer = ask_question(req.question)
    return AnswerResponse(question=req.question, answer=answer) 
    