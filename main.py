from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import anthropic
import os
from datetime import datetime

app = FastAPI(
    title="Assistente Educacional API",
    description="API para assistente educacional com IA",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join("frontend", "index.html"))


# Cliente Anthropic
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    subject: str
    question: str
    context: Optional[str] = None
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    answer: str
    subject: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str

# Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Verifica saúde da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal para interação com o assistente educacional
    """
    try:
        # Construir prompt educacional
        system_prompt = f"""Você é um assistente educacional especializado em {request.subject}.
        
Suas responsabilidades:
- Explicar conceitos de forma clara e didática
- Usar exemplos práticos e relevantes
- Adaptar a linguagem ao nível do estudante
- Estimular o pensamento crítico
- Fornecer recursos adicionais quando apropriado

Mantenha suas respostas:
- Educativas e encorajadoras
- Estruturadas e organizadas
- Com exemplos quando necessário
- Focadas no aprendizado efetivo"""

        # Construir mensagens
        messages = []
        
        # Adicionar histórico se existir
        if request.history:
            for msg in request.history:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Adicionar contexto se fornecido
        user_message = request.question
        if request.context:
            user_message = f"Contexto: {request.context}\n\nPergunta: {request.question}"
        
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Chamar Claude API
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=system_prompt,
            messages=messages
        )
        
        answer = response.content[0].text
        
        return {
            "answer": answer,
            "subject": request.subject,
            "timestamp": datetime.now().isoformat()
        }
        
    except anthropic.APIError as e:
        raise HTTPException(status_code=500, detail=f"Erro na API Claude: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/api/subjects")
async def get_subjects():
    """Retorna lista de disciplinas suportadas"""
    subjects = [
        
    ]
    return {"subjects": subjects}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)