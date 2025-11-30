# tests/conftest.py
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

# -----------------------------
# Client para testes
# -----------------------------
@pytest.fixture(scope="session")
def client():
    return TestClient(app)

# -----------------------------
# Variáveis de ambiente
# -----------------------------
@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-api-key")
    monkeypatch.setenv("ENVIRONMENT", "test")
    yield

# -----------------------------
# Mock do Gemini
# -----------------------------
@pytest.fixture
def mock_gemini():
    with patch("main.model") as mock:
        fake_response = MagicMock()
        fake_response.text = "Resposta simulada Gemini"
        mock.generate_content.return_value = fake_response
        yield mock

# -----------------------------
# Requests exemplo
# -----------------------------
@pytest.fixture
def sample_chat_request():
    return {
        "subject": "Matemática",
        "question": "Explique números primos",
        "history": []
    }

@pytest.fixture
def sample_chat_with_history():
    return {
        "subject": "Física",
        "question": "Explique velocidade",
        "context": "cinemática",
        "history": [
            {"role": "user", "content": "O que é movimento?"},
            {"role": "assistant", "content": "Movimento é..."}
        ]
    }
