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

def ask_about_document(document: str, question: str) -> str:
    """Responde a uma pergunta com base apenas no texto do documento."""
    prompt = f"DOCUMENTO:\n{document}\n\nPERGUNTA:\n{question}"

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,

config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )

    return response.text

if __name__ == "__main__":
    texto = (
        "A Maria nasceu em 1995, em Recife. Trabalha como engenheira de software "
        "na empresa Acme desde 2020 e gosta de fotografia."
    )
    print(ask_about_document(texto, "Onde a Maria trabalha?"))
    print(ask_about_document(texto, "Qual é o salário da Maria?"))