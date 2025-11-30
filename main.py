from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from google import genai

app = FastAPI()

# Inicialização segura do cliente
try:
    client = genai.Client()
    model = client.GenerativeModel("gemini-2.5-flash")
except Exception:
    model = None


class QuestionRequest(BaseModel):
    subject: str
    question: str
    context: str | None = ""
    history: list | None = []


@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/api/chat")
def chat(request: QuestionRequest):
    if not model:
        raise HTTPException(status_code=503, detail="Modelo indisponível no momento.")

    prompt = f"""
Você é um tutor especializado em {request.subject}.
Responda de forma didática, com exemplos, explicando passo a passo.

Pergunta do aluno:
{request.question}

Contexto adicional:
{request.context}
"""

    try:
        response = model.generate_content(prompt)
        answer = getattr(response, "text", None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")

    if not answer:
        raise HTTPException(status_code=500, detail="Falha ao gerar resposta.")

    return {"answer": answer}
