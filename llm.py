from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = "gemini-3.5-flash-lite"

client = genai.Client()

SYSTEM_PROMPT = """Você é um assistente que responde perguntas sobre um documento.
Regras:
- Responda usando SOMENTE as informações do documento fornecido.
- Se a resposta não estiver no documento, diga: "Não encontrei essa informação no documento."
- Responda em português, de forma clara e curta."""

CONFIG = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)


def build_prompt(document: str, question: str) -> str:
    return f"DOCUMENTO:\n{document}\n\nPERGUNTA:\n{question}"


def ask_about_document(document: str, question: str) -> str:
    """Responde a uma pergunta com base apenas no texto do documento."""
    response = client.models.generate_content(
        model=MODEL,
        contents=build_prompt(document, question),
        config=CONFIG,
    )
    return response.text


def stream_answer(document: str, question: str):
    """Gera a resposta aos pedaços, conforme o modelo escreve."""
    for chunk in client.models.generate_content_stream(
        model=MODEL,
        contents=build_prompt(document, question),
        config=CONFIG,
    ):
        if chunk.text:
            yield chunk.text


if __name__ == "__main__":
    texto = (
        "A Maria nasceu em 1995, em Recife. Trabalha como engenheira de software "
        "na empresa Acme desde 2020 e gosta de fotografia."
    )
    print(ask_about_document(texto, "Onde a Maria trabalha?"))
    print(ask_about_document(texto, "Qual é o salário da Maria?"))