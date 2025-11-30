# tests/test_main.py
from datetime import datetime

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    datetime.fromisoformat(data["timestamp"])

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code in [200, 307, 404]

def test_get_subjects(client):
    response = client.get("/api/subjects")
    assert response.status_code == 200

    subjects = response.json()["subjects"]
    assert len(subjects) > 0

    s = subjects[0]
    assert "id" in s and "name" in s and "icon" in s

def test_chat_success(client, mock_gemini, sample_chat_request):
    response = client.post("/api/chat", json=sample_chat_request)
    assert response.status_code == 200

    data = response.json()
    assert "answer" in data
    assert "subject" in data
    assert "timestamp" in data

def test_chat_with_history(client, mock_gemini, sample_chat_with_history):
    response = client.post("/api/chat", json=sample_chat_with_history)
    assert response.status_code == 200

    data = response.json()
    assert "answer" in data
    assert "timestamp" in data

def test_chat_missing_subject(client, mock_gemini):
    payload = {
        "subject": "",
        "question": "aaa",
        "history": []
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 422

def test_chat_missing_question(client, mock_gemini):
    payload = {
        "subject": "Programação",
        "history": []
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 422
