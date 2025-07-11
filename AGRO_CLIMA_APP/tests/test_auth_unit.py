import pytest
from app import auth
from datetime import datetime, timedelta
from jose import jwt

# Configuración igual a auth.py
SECRET_KEY = "secreto"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def test_verify_password():
    # Hashea una contraseña y verifica
    plain_password = "test123"
    hashed_password = auth.pwd_context.hash(plain_password)

    assert auth.verify_password(plain_password, hashed_password)
    assert not auth.verify_password("wrong", hashed_password)


def test_authenticate_user_success(monkeypatch):
    # Simulamos un usuario en base de datos
    class DummyUser:
        username = "admin"
        hashed_password = auth.pwd_context.hash("admin")

    class DummyDB:
        def query(self, model):
            class Query:
                def filter(self, condition):
                    return self
                def first(self):
                    return DummyUser()
            return Query()

    db = DummyDB()
    result = auth.authenticate_user(db, "admin", "admin")
    assert result.username == "admin"

def test_authenticate_user_fail(monkeypatch):
    # Usuario inexistente
    class DummyDB:
        def query(self, model):
            class Query:
                def filter(self, condition):
                    return self
                def first(self):
                    return None
            return Query()

    db = DummyDB()
    result = auth.authenticate_user(db, "user", "pass")
    assert result is None


def test_create_access_token():
    data = {"sub": "admin"}
    token = auth.create_access_token(data)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "admin"
    assert "exp" in decoded
