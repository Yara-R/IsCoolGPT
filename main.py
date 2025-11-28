from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import google.generativeai as genai
import os

# ---------------------------
# CONFIGURAÇÃO INICIAL
# ---------------------------

app = FastAPI(
    title="Assistente Educacional API",
    description="API para assistente educacional com IA",
    version="1.0.0"
)

# CORS liberado para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir frontend estático
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join("frontend", "index.html"))


# ---------------------------
# CONFIGURAR GEMINI
# ---------------------------

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


# ---------------------------
# MODELOS Pydantic
# ---------------------------

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    subject: str
    question: str
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    answer: str
    subject: str
    timestamp: str


# ---------------------------
# ENDPOINT: LISTA DE DISCIPLINAS
# ---------------------------

@app.get("/api/subjects")
async def get_subjects():
    subjects = [
        {"id": "intro_comp", "name": "Introdução à Computação", "icon": "💻"},
        {"id": "prog1", "name": "Fundamentos de Programação", "icon": "👨‍💻"},
        {"id": "logica", "name": "Lógica Matemática", "icon": "🧠"},
        {"id": "matematica", "name": "Matemática para Computação", "icon": "📐"},
        {"id": "poo", "name": "Programação Orientada a Objetos", "icon": "📦"},
        {"id": "bd", "name": "Banco de Dados", "icon": "🗄️"},
        {"id": "redes", "name": "Redes de Computadores", "icon": "🌐"},
        {"id": "so", "name": "Sistemas Operacionais", "icon": "🖥️"},
        {"id": "seg_info", "name": "Segurança da Informação", "icon": "🔐"},
    ]
    return {"subjects": subjects}


# ---------------------------
# ENDPOINT: CHAT (COM GEMINI)
# ---------------------------

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        subject = request.subject
        question = request.question

        prompt = f"""
Você é um tutor especializado em {subject}.
Responda de forma didática, com exemplos, explicando passo a passo.

Pergunta do aluno:
{question}
"""

        response = model.generate_content(prompt)

        # resposta segura
        answer = getattr(response, "text", None) or "Não foi possível gerar resposta."

        return {
            "answer": answer,
            "subject": subject,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print("ERRO NO CHAT:", str(e))
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


# ---------------------------

@app.get("/health")
def health():
    return {"status": "ok"}

# ---------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
