from fastapi import FastAPI
from rag.retriever import retrieve
from rag.generator import generate

app = FastAPI(title="Loan RAG Assistant")

@app.get("/")
def health():
    return {"status":"running"}

@app.post("/chat")
def chat(question:str):
    context = retrieve(question)
    answer = generate(question, context)
    return {
        "answer": answer,
        "context": context
    }
