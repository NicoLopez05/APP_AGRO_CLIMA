from fastapi.testclient import TestClient
from app.main import app
from app import auth  # ← se importa el módulo que contiene authenticate_user
import pytest

client = TestClient(app)

def test_login_fail():
    response = client.post("/auth/login", data={
        "username": "usuario_no_existente",
        "password": "password_valido123",
        "grant_type": "password"
    })
    print(response.text)
    assert response.status_code == 401



def test_login_success(monkeypatch):
    class DummyUser:
        id = 1
        username = "admin"
        full_name = "Admin"
        hashed_password = "hashed"

    def mock_authenticate_user(db, username, password):      
        return DummyUser()

    def mock_create_access_token(data):
        return "abc123"

    monkeypatch.setattr(auth, "authenticate_user", mock_authenticate_user)
    monkeypatch.setattr(auth, "create_access_token", mock_create_access_token)

    response = client.post("/auth/login", data={
        "username": "admin",
        "password": "admin",
        "grant_type": "password"
    })

    assert response.status_code == 200
    assert response.json()["access_token"] == "abc123"
