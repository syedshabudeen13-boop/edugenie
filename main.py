from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


# --------------------------------------------------
# Static files and templates
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


class QARequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


class LearningRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    level: str = Field(
        default="beginner",
        max_length=50
    )


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }


# --------------------------------------------------
# Question and Answer
# --------------------------------------------------

@app.post("/qa")
async def qa(payload: QARequest):

    result = answer_question(
        payload.question
    )

    return {
        "result": result
    }


# --------------------------------------------------
# Explain Topic
# --------------------------------------------------

@app.post("/explain")
async def explain(payload: TextRequest):

    result = explain_topic(
        payload.text
    )

    return {
        "result": result
    }


# --------------------------------------------------
# Generate Quiz
# --------------------------------------------------

@app.post("/quiz")
async def quiz(payload: QuizRequest):

    result = generate_quiz(
        payload.text
    )

    return {
        "result": result
    }


# --------------------------------------------------
# Summarize Text
# --------------------------------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    result = summarize_text(
        payload.text
    )

    return {
        "result": result
    }


# --------------------------------------------------
# Learning Recommendations
# --------------------------------------------------

@app.post("/learn/recommendations")
async def learn(payload: LearningRequest):

    result = get_learning_recommendations(
        payload.topic,
        payload.level
    )

    return {
        "result": result
    }