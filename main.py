from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from llm import ask_about_document, stream_answer

app = FastAPI(title="DocChat")


class AskRequest(BaseModel):
    document: str = Field(max_length=20000)
    question: str = Field(max_length=500)


class AskResponse(BaseModel):
    answer: str


def validate(request: AskRequest) -> None:
    if not request.document.strip() or not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Documento e pergunta não podem estar vazios.",
        )


def safe_stream(document: str, question: str):
    try:
        yield from stream_answer(document, question)
    except Exception:
        yield "\n\n[Erro ao consultar o modelo de IA. Tente novamente.]"


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/app/")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    validate(request)

    try:
        answer = ask_about_document(request.document, request.question)
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Erro ao consultar o modelo de IA. Tente novamente.",
        )

    return AskResponse(answer=answer)


@app.post("/ask/stream")
def ask_stream(request: AskRequest):
    validate(request)
    return StreamingResponse(
        safe_stream(request.document, request.question),
        media_type="text/plain; charset=utf-8",
    )


app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")