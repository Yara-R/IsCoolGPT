import pytest
from unittest.mock import Mock
import os
import sys

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_response():
    """Fixture para mock de resposta do Claude"""
    mock_response = Mock()
    mock_content = Mock()
    mock_content.text = "Esta é uma resposta mockada do Gemini"
    mock_response.content = [mock_content]
    return mock_response

@pytest.fixture
def sample_chat_request():
    """Fixture com request de chat padrão"""
    return {
        "subject": "Matemática",
        "question": "O que é um número primo?",
        "context": None,
        "history": []
    }

@pytest.fixture
def sample_chat_with_history():
    """Fixture com request incluindo histórico"""
    return {
        "subject": "Física",
        "question": "E sobre velocidade?",
        "context": "Estou estudando cinemática",
        "history": [
            {"role": "user", "content": "O que é movimento?"},
            {"role": "assistant", "content": "Movimento é a mudança de posição..."}
        ]
    }

@pytest.fixture
def mock_env_vars(monkeypatch):
    """Fixture para configurar variáveis de ambiente de teste"""
    monkeypatch.setenv("GOOGLE_API_KEY", "test-api-key-12345")
    monkeypatch.setenv("ENVIRONMENT", "test")

@pytest.fixture(autouse=True)
def setup_test_env(mock_env_vars):
    """Configuração automática de ambiente de teste"""
    pass

# ============================================
# Testes para fixtures
# ============================================

def test_mock_response(mock_response):
    """Testa a fixture mock_response"""
    assert mock_response.content[0].text == "Esta é uma resposta mockada do Gemini"

def test_sample_chat_request(sample_chat_request):
    """Testa a fixture sample_chat_request"""
    assert sample_chat_request["subject"] == "Matemática"
    assert sample_chat_request["question"] == "O que é um número primo?"
    assert sample_chat_request["context"] is None
    assert isinstance(sample_chat_request["history"], list)

def test_sample_chat_with_history(sample_chat_with_history):
    """Testa a fixture sample_chat_with_history"""
    assert sample_chat_with_history["subject"] == "Física"
    assert sample_chat_with_history["question"] == "E sobre velocidade?"
    assert sample_chat_with_history["context"] == "Estou estudando cinemática"
    assert len(sample_chat_with_history["history"]) == 2

def test_env_vars(mock_env_vars):
    """Testa se as variáveis de ambiente estão configuradas corretamente"""
    assert os.getenv("GOOGLE_API_KEY") == "test-api-key-12345"
    assert os.getenv("ENVIRONMENT") == "test"# ============================================
# Testes para fixtures
# ============================================

def test_mock_response(mock_response):
    """Testa a fixture mock_response"""
    assert mock_response.content[0].text == "Esta é uma resposta mockada do Gemini"
    assert isinstance(mock_response.content, list)  # BEGIN:
    assert len(mock_response.content) == 1  # END:

def test_sample_chat_request(sample_chat_request):
    """Testa a fixture sample_chat_request"""
    assert sample_chat_request["subject"] == "Matemática"
    assert sample_chat_request["question"] == "O que é um número primo?"
    assert sample_chat_request["context"] is None
    assert isinstance(sample_chat_request["history"], list)
    assert len(sample_chat_request["history"]) == 0  # BEGIN:

def test_sample_chat_with_history(sample_chat_with_history):
    """Testa a fixture sample_chat_with_history"""
    assert sample_chat_with_history["subject"] == "Física"
    assert sample_chat_with_history["question"] == "E sobre velocidade?"
    assert sample_chat_with_history["context"] == "Estou estudando cinemática"
    assert len(sample_chat_with_history["history"]) == 2
    assert sample_chat_with_history["history"][0]["role"] == "user"  # BEGIN:
    assert sample_chat_with_history["history"][1]["content"] == "Movimento é a mudança de posição..."  # END:

def test_env_vars(mock_env_vars):
    """Testa se as variáveis de ambiente estão configuradas corretamente"""
    assert os.getenv("GOOGLE_API_KEY") == "test-api-key-12345"
    assert os.getenv("ENVIRONMENT") == "test"
    assert os.getenv("NON_EXISTENT_VAR") is None  # BEGIN:
