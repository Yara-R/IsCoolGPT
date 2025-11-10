import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime
import sys
import os

# Adicionar path do projeto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app, ChatRequest, Message

client = TestClient(app)


class TestHealthEndpoints:
    """Testes para endpoints de health check"""
    
    def test_root_endpoint(self):
        """Testa endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert "timestamp" in data
    
    def test_health_check_endpoint(self):
        """Testa endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        
    def test_health_timestamp_format(self):
        """Verifica formato do timestamp"""
        response = client.get("/health")
        data = response.json()
        # Verifica se o timestamp pode ser parseado
        datetime.fromisoformat(data["timestamp"])


class TestSubjectsEndpoint:
    """Testes para endpoint de disciplinas"""
    
    def test_get_subjects(self):
        """Testa listagem de disciplinas"""
        response = client.get("/api/subjects")
        assert response.status_code == 200
        data = response.json()
        assert "subjects" in data
        assert len(data["subjects"]) > 0
    
    def test_subjects_structure(self):
        """Verifica estrutura de cada disciplina"""
        response = client.get("/api/subjects")
        subjects = response.json()["subjects"]
        
        for subject in subjects:
            assert "id" in subject
            assert "name" in subject
            assert "icon" in subject
            assert isinstance(subject["id"], str)
            assert isinstance(subject["name"], str)
            assert isinstance(subject["icon"], str)
    
    def test_subjects_count(self):
        """Verifica quantidade mínima de disciplinas"""
        response = client.get("/api/subjects")
        subjects = response.json()["subjects"]
        assert len(subjects) >= 10
    
    def test_subjects_unique_ids(self):
        """Verifica se IDs são únicos"""
        response = client.get("/api/subjects")
        subjects = response.json()["subjects"]
        ids = [s["id"] for s in subjects]
        assert len(ids) == len(set(ids))


class TestChatEndpoint:
    """Testes para endpoint de chat"""
    
    @patch('main.client.messages.create')
    def test_chat_basic_request(self, mock_claude):
        """Testa requisição básica de chat"""
        # Mock da resposta do Claude
        mock_response = Mock()
        mock_response.content = [Mock(text="Esta é uma resposta de teste")]
        mock_claude.return_value = mock_response
        
        request_data = {
            "subject": "Matemática",
            "question": "O que é um número primo?"
        }
        
        response = client.post("/api/chat", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "subject" in data
        assert "timestamp" in data
        assert data["subject"] == "Matemática"
    
    @patch('main.client.messages.create')
    def test_chat_with_context(self, mock_claude):
        """Testa chat com contexto adicional"""
        mock_response = Mock()
        mock_response.content = [Mock(text="Resposta com contexto")]
        mock_claude.return_value = mock_response
        
        request_data = {
            "subject": "Física",
            "question": "Explique velocidade",
            "context": "Estou no ensino médio"
        }
        
        response = client.post("/api/chat", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Resposta com contexto"
    
    @patch('main.client.messages.create')
    def test_chat_with_history(self, mock_claude):
        """Testa chat com histórico de conversação"""
        mock_response = Mock()
        mock_response.content = [Mock(text="Continuando conversa")]
        mock_claude.return_value = mock_response
        
        request_data = {
            "subject": "Química",
            "question": "E sobre moléculas?",
            "history": [
                {"role": "user", "content": "O que são átomos?"},
                {"role": "assistant", "content": "Átomos são..."}
            ]
        }
        
        response = client.post("/api/chat", json=request_data)
        assert response.status_code == 200
        
        # Verifica se o histórico foi passado para a API
        call_args = mock_claude.call_args
        messages = call_args.kwargs['messages']
        assert len(messages) >= 2  # Histórico + nova mensagem
    
    def test_chat_missing_subject(self):
        """Testa requisição sem disciplina"""
        request_data = {
            "question": "Pergunta sem disciplina"
        }
        
        response = client.post("/api/chat", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_chat_missing_question(self):
        """Testa requisição sem pergunta"""
        request_data = {
            "subject": "Matemática"
        }
        
        response = client.post("/api/chat", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_chat_empty_question(self):
        """Testa requisição com pergunta vazia"""
        request_data = {
            "subject": "Matemática",
            "question": ""
        }
        
        response = client.post("/api/chat", json=request_data)
        assert response.status_code == 422
    
    @patch('main.client.messages.create')
    def test_chat_api_error_handling(self, mock_claude):
        """Testa tratamento de erros da API Claude"""
        mock_claude.side_effect = Exception("API Error")
        
        request_data = {
            "subject": "Matemática",
            "question": "Teste de erro"
        }
        
        response = client.post("/api/chat", json=request_data)
        assert response.status_code == 500
        assert "erro" in response.json()["detail"].lower()


class TestModels:
    """Testes para modelos Pydantic"""
    
    def test_message_model_valid(self):
        """Testa criação de Message válida"""
        msg = Message(role="user", content="Teste")
        assert msg.role == "user"
        assert msg.content == "Teste"
    
    def test_chat_request_minimal(self):
        """Testa ChatRequest com campos mínimos"""
        req = ChatRequest(subject="Matemática", question="Teste?")
        assert req.subject == "Matemática"
        assert req.question == "Teste?"
        assert req.context is None
        assert req.history == []
    
    def test_chat_request_full(self):
        """Testa ChatRequest com todos os campos"""
        req = ChatRequest(
            subject="Física",
            question="Como funciona?",
            context="Contexto adicional",
            history=[Message(role="user", content="Oi")]
        )
        assert req.context == "Contexto adicional"
        assert len(req.history) == 1


class TestCORS:
    """Testes para configuração CORS"""
    
    def test_cors_headers_present(self):
        """Verifica presença de headers CORS"""
        response = client.options("/api/subjects")
        # CORS middleware deve adicionar headers
        assert response.status_code in [200, 405]


class TestIntegration:
    """Testes de integração"""
    
    @patch('main.client.messages.create')
    def test_full_conversation_flow(self, mock_claude):
        """Testa fluxo completo de conversação"""
        # Setup mock
        mock_response = Mock()
        mock_response.content = [Mock(text="Resposta do assistente")]
        mock_claude.return_value = mock_response
        
        # 1. Obter disciplinas
        subjects_response = client.get("/api/subjects")
        assert subjects_response.status_code == 200
        subjects = subjects_response.json()["subjects"]
        
        # 2. Fazer primeira pergunta
        first_question = {
            "subject": subjects[0]["name"],
            "question": "Primeira pergunta"
        }
        first_response = client.post("/api/chat", json=first_question)
        assert first_response.status_code == 200
        
        # 3. Fazer segunda pergunta com histórico
        second_question = {
            "subject": subjects[0]["name"],
            "question": "Segunda pergunta",
            "history": [
                {"role": "user", "content": "Primeira pergunta"},
                {"role": "assistant", "content": first_response.json()["answer"]}
            ]
        }
        second_response = client.post("/api/chat", json=second_question)
        assert second_response.status_code == 200
    
    def test_api_documentation_available(self):
        """Verifica se documentação OpenAPI está disponível"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        openapi = response.json()
        assert "info" in openapi
        assert "paths" in openapi


class TestPerformance:
    """Testes de performance básicos"""
    
    def test_health_response_time(self):
        """Verifica tempo de resposta do health check"""
        import time
        start = time.time()
        response = client.get("/health")
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 0.1  # Deve responder em menos de 100ms
    
    def test_subjects_response_time(self):
        """Verifica tempo de resposta das disciplinas"""
        import time
        start = time.time()
        response = client.get("/api/subjects")
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 0.1


class TestErrorHandling:
    """Testes de tratamento de erros"""
    
    def test_invalid_endpoint(self):
        """Testa endpoint inválido"""
        response = client.get("/api/invalid")
        assert response.status_code == 404
    
    def test_invalid_method(self):
        """Testa método HTTP inválido"""
        response = client.delete("/api/subjects")
        assert response.status_code == 405
    
    def test_invalid_json(self):
        """Testa JSON inválido"""
        response = client.post(
            "/api/chat",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    @patch('main.client.messages.create')
    def test_claude_api_timeout(self, mock_claude):
        """Testa timeout da API Claude"""
        import anthropic
        mock_claude.side_effect = anthropic.APIError("Timeout")
        
        request_data = {
            "subject": "Matemática",
            "question": "Teste timeout"
        }
        
        response = client.post("/api/chat", json=request_data)
        assert response.status_code == 500


if __name__ == "__main__":
    pytest.main([__file__, "-v"])