import pytest
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

# ============================================
# Fixtures
# ============================================

@pytest.fixture(autouse=True)
def setup_env():
    """Setup de variáveis de ambiente"""
    os.environ["GOOGLE_API_KEY"] = "test-api-key-12345"
    os.environ["ENVIRONMENT"] = "test"
    yield

@pytest.fixture
def mock_gemini():
    """Mock do Google Gemini"""
    with patch('main.model') as mock:
        mock_response = MagicMock()
        mock_response.text = "Esta é uma resposta simulada do Gemini."
        mock.generate_content.return_value = mock_response
        yield mock

# ============================================
# Testes de Health
# ============================================

def test_health_endpoint():
    """Testa endpoint de health"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data

# ============================================
# Testes de Root
# ============================================

def test_root_endpoint():
    """Testa endpoint raiz"""
    response = client.get("/")
    assert response.status_code in [200, 307, 404]

# ============================================
# Testes de Subjects
# ============================================

def test_get_subjects():
    """Testa listagem de disciplinas"""
    response = client.get("/api/subjects")
    assert response.status_code == 200
    data = response.json()
    assert "subjects" in data
    assert len(data["subjects"]) > 0
    
    # Validar estrutura
    subject = data["subjects"][0]
    assert "id" in subject
    assert "name" in subject
    assert "icon" in subject

# ============================================
# Testes de Chat
# ============================================

def test_chat_success(mock_gemini):
    """Testa chat com sucesso"""
    payload = {
        "subject": "Matemática Computacional",
        "question": "O que é um algoritmo?",
        "history": []
    }
    
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "subject" in data
    assert "timestamp" in data

def test_chat_with_context(mock_gemini):
    """Testa chat com contexto"""
    payload = {
        "subject": "Programação",
        "question": "O que é uma função?",
        "context": "Estudando Python básico",
        "history": []
    }
    
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "subject" in data
    assert "timestamp" in data

def test_chat_invalid_subject():
    """Testa chat com assunto inválido"""
    payload = {
        "subject": "",
        "question": "O que é uma função?",
        "history": []
    }
    
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_chat_missing_question():
    """Testa chat sem pergunta"""
    payload = {
        "subject": "Programação",
        "history": []
    }
    
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, Mock
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)
