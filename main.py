from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from llm import ask_about_document

app = FastAPI(title="DocChat")


class AskRequest(BaseModel):
    document: str
    question: str


class AskResponse(BaseModel):
    answer: str


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    if not request.document.strip() or not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Documento e pergunta não podem estar vazios.",
        )

    try:
        answer = ask_about_document(request.document, request.question)
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Erro ao consultar o modelo de IA. Tente novamente.",
        )

    return AskResponse(answer=answer)