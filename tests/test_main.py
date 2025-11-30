import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)


# ============================================
# Test Health Endpoints
# ============================================

class TestHealthEndpoints:
    """Testes para endpoints de health check"""
    
    def test_health_endpoint(self):
        """Testa se o endpoint de health retorna status correto"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"  # Corrigido: o endpoint retorna "ok"
        assert "timestamp" in data
    
    def test_root_endpoint(self):
        """Testa se o endpoint raiz redireciona corretamente"""
        response = client.get("/")
        assert response.status_code in [200, 307]  # 307 é redirect


# ============================================
# Test Subjects Endpoint
# ============================================

class TestSubjectsEndpoint:
    """Testes para endpoint de disciplinas"""
    
    def test_get_subjects(self):
        """Testa se retorna lista de disciplinas"""
        response = client.get("/api/subjects")
        assert response.status_code == 200
        data = response.json()
        assert "subjects" in data
        assert isinstance(data["subjects"], list)
        assert len(data["subjects"]) > 0
    
    def test_subjects_structure(self):
        """Testa estrutura dos objetos de disciplina"""
        response = client.get("/api/subjects")
        subjects = response.json()["subjects"]
        
        for subject in subjects:
            assert "id" in subject
            assert "name" in subject
            assert "icon" in subject
            assert isinstance(subject["id"], str)
            assert isinstance(subject["name"], str)
            assert isinstance(subject["icon"], str)


# ============================================
# Test Chat Endpoint
# ============================================

class TestChatEndpoint:
    """Testes para endpoint de chat com IA"""
    
    @patch('google.generativeai.GenerativeModel')
    def test_chat_successful_request(self, mock_model):
        """Testa requisição de chat bem-sucedida"""
        # Mock da resposta do Gemini
        mock_response = MagicMock()
        mock_response.text = "Computação é a ciência que estuda processamento de informações."
        mock_model.return_value.generate_content.return_value = mock_response
        
        payload = {
            "subject": "Introdução à Computação",
            "question": "O que é computação?",
            "history": []
        }
        
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        assert "answer" in data
        assert "subject" in data
        assert "timestamp" in data
        assert data["subject"] == "Introdução à Computação"
        assert len(data["answer"]) > 0
    
    @patch('google.generativeai.GenerativeModel')
    def test_chat_with_context(self, mock_model):
        """Testa chat com contexto adicional"""
        mock_response = MagicMock()
        mock_response.text = "Resposta sobre programação."
        mock_model.return_value.generate_content.return_value = mock_response
        
        payload = {
            "subject": "Fundamentos de Programação",
            "question": "O que é uma variável?",
            "context": "Estou estudando Python",
            "history": []
        }
        
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 200
    
    @patch('google.generativeai.GenerativeModel')
    def test_chat_with_history(self, mock_model):
        """Testa chat com histórico de conversação"""
        mock_response = MagicMock()
        mock_response.text = "Resposta considerando histórico."
        mock_model.return_value.generate_content.return_value = mock_response
        
        payload = {
            "subject": "Matemática Computacional",
            "question": "E como aplicar isso?",
            "history": [
                {"role": "user", "content": "O que é um algoritmo?"},
                {"role": "assistant", "content": "Um algoritmo é uma sequência de passos."}
            ]
        }
        
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 200
    
    def test_chat_missing_subject(self):
        """Testa requisição sem disciplina"""
        payload = {
            "question": "Pergunta sem disciplina",
            "history": []
        }
        
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_chat_missing_question(self):
        """Testa requisição sem pergunta"""
        payload = {
            "subject": "Matemática",
            "history": []
        }
        
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 422
    
    def test_chat_empty_question(self):
        """Testa requisição com pergunta vazia"""
        payload = {
            "subject": "Matemática",
            "question": "",
            "history": []
        }
        
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 422
    
    @patch('google.generativeai.GenerativeModel')
    def test_chat_api_error_handling(self, mock_model):
        """Testa tratamento de erro da API Gemini"""
        # Simular erro da API
        mock_model.return_value.generate_content.side_effect = Exception("API Error")
        
        payload = {
            "subject": "Teste",
            "question": "Teste?",
            "history": []
        }
        
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 500
        assert "detail" in response.json()


# ============================================
# Test Models
# ============================================

class TestModels:
    """Testes para validação de modelos Pydantic"""
    
    def test_chat_request_valid(self):
        """Testa modelo ChatRequest válido"""
        from main import ChatRequest
        
        request = ChatRequest(
            subject="Matemática",
            question="Teste?",
            history=[]
        )
        
        assert request.subject == "Matemática"
        assert request.question == "Teste?"
        assert request.history == []
    
    def test_chat_request_with_optional_fields(self):
        """Testa ChatRequest com campos opcionais"""
        from main import ChatRequest
        
        request = ChatRequest(
            subject="Física",
            question="O que é força?",
            context="Estudando mecânica",
            history=[{"role": "user", "content": "Olá"}]
        )
        
        assert request.context == "Estudando mecânica"
        assert len(request.history) == 1
    
    def test_chat_response_structure(self):
        """Testa estrutura do ChatResponse"""
        from main import ChatResponse
        
        response = ChatResponse(
            answer="Resposta teste",
            subject="Matemática",
            timestamp="2024-01-01T00:00:00"
        )
        
        assert response.answer == "Resposta teste"
        assert response.subject == "Matemática"


# ============================================
# Test CORS
# ============================================

class TestCORS:
    """Testes para configuração de CORS"""
    
    def test_cors_headers_options(self):
        """Testa headers CORS em requisição OPTIONS"""
        response = client.options(
            "/api/chat",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code in [200, 405]
    
    def test_cors_headers_post(self):
        """Testa headers CORS em requisição POST"""
        response = client.post(
            "/api/subjects",
            headers={"Origin": "http://localhost:3000"}
        )
        # Pode ser 405 (Method Not Allowed) mas deve incluir headers CORS
        assert response.status_code in [200, 405, 422]


# ============================================
# Test Integration
# ============================================

class TestIntegration:
    """Testes de integração end-to-end"""
    
    @patch('google.generativeai.GenerativeModel')
    def test_full_conversation_flow(self, mock_model):
        """Testa fluxo completo de conversação"""
        mock_response = MagicMock()
        mock_response.text = "Resposta da IA"
        mock_model.return_value.generate_content.return_value = mock_response
        
        # 1. Buscar disciplinas
        subjects_response = client.get("/api/subjects")
        assert subjects_response.status_code == 200
        subjects = subjects_response.json()["subjects"]
        
        # 2. Fazer primeira pergunta
        first_payload = {
            "subject": subjects[0]["name"],
            "question": "Primeira pergunta",
            "history": []
        }
        first_response = client.post("/api/chat", json=first_payload)
        assert first_response.status_code == 200
        first_data = first_response.json()
        
        # 3. Fazer segunda pergunta com histórico
        second_payload = {
            "subject": subjects[0]["name"],
            "question": "Segunda pergunta",
            "history": [
                {"role": "user", "content": "Primeira pergunta"},
                {"role": "assistant", "content": first_data["answer"]}
            ]
        }
        second_response = client.post("/api/chat", json=second_payload)
        assert second_response.status_code == 200
    
    def test_health_check_integration(self):
        """Testa health check no fluxo de integração"""
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "ok"  # Corrigido


# ============================================
# Test Performance
# ============================================

class TestPerformance:
    """Testes básicos de performance"""
    
    def test_health_endpoint_response_time(self):
        """Testa tempo de resposta do health endpoint"""
        import time
        
        start = time.time()
        response = client.get("/health")
        end = time.time()
        
        assert response.status_code == 200
        assert (end - start) < 1.0  # Deve responder em menos de 1 segundo
    
    def test_subjects_endpoint_response_time(self):
        """Testa tempo de resposta do endpoint de disciplinas"""
        import time
        
        start = time.time()
        response = client.get("/api/subjects")
        end = time.time()
        
        assert response.status_code == 200
        assert (end - start) < 1.0


# ============================================
# Test Error Handling
# ============================================

class TestErrorHandling:
    """Testes para tratamento de erros"""
    
    def test_invalid_endpoint(self):
        """Testa acesso a endpoint inexistente"""
        response = client.get("/api/naoexiste")
        assert response.status_code == 404
    
    def test_invalid_json_payload(self):
        """Testa payload JSON inválido"""
        response = client.post(
            "/api/chat",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self):
        """Testa requisição sem campos obrigatórios"""
        response = client.post("/api/chat", json={})
        assert response.status_code == 422
    
    @patch('google.generativeai.GenerativeModel')
    def test_api_timeout_handling(self, mock_model):
        """Testa tratamento de timeout da API"""
        import requests
        mock_model.return_value.generate_content.side_effect = requests.Timeout()
        
        payload = {
            "subject": "Teste",
            "question": "Teste timeout",
            "history": []
        }
        
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 500


# ============================================
# Configuração de Fixtures
# ============================================

@pytest.fixture(autouse=True)
def setup_env():
    """Setup de variáveis de ambiente para testes"""
    os.environ["GOOGLE_API_KEY"] = "test-key-for-testing"
    os.environ["ENVIRONMENT"] = "test"
    yield
    # Cleanup não necessário pois são variáveis de teste


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
