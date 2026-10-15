from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
from rag.loader import load_demo_document
from rag.pipeline import answer_question

app = FastAPI(title="Loan Rules Retrieval Demo", version="0.3.0")
WEB_DIR = Path(__file__).resolve().parents[1] / "web"

class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)

    @field_validator("question")
    @classmethod
    def check_question(cls, value):
        if not value.strip():
            raise ValueError("question must not be blank")
        return value.strip()

@app.get("/")
def home():
    return FileResponse(WEB_DIR / "index.html")

@app.get("/healthz")
def health():
    document = load_demo_document()
    return {"status": "ok", "version": "0.3.0", "data_mode": "sample", "sections": len(document["sections"])}

@app.get("/api/documents/{document_id}")
def get_document(document_id: str):
    document = load_demo_document()
    if document_id != document["id"]:
        raise HTTPException(status_code=404, detail="Document not found")
    return {**document, "sections": [{"id": section["id"], "title": section["title"], "text": section["text"], "position": index + 1} for index, section in enumerate(document["sections"])]}

@app.post("/api/chat")
def chat(body: ChatRequest):
    return answer_question(body.question)

@app.post("/chat", include_in_schema=False)
def legacy_chat(question: str = Query(min_length=1, max_length=500)):
    return answer_question(question)

app.mount("/assets", StaticFiles(directory=WEB_DIR), name="assets")
