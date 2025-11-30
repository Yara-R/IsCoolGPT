import pytest
from unittest.mock import Mock
import os
import sys

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


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
def mock_env_vars(monkeypatch):
    """Fixture para configurar variáveis de ambiente de teste"""
    monkeypatch.setenv("GOOGLE_API_KEY", "test-api-key-12345")
    monkeypatch.setenv("ENVIRONMENT", "test")


@pytest.fixture(autouse=True)
def setup_test_env(mock_env_vars):
    """Configuração automática de ambiente de teste"""
    pass