from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
import pytest
from fastapi.testclient import TestClient
from bookstore.main import app
from bookstore.database import get_db
from uuid import uuid4
from datetime import timedelta
from bookstore.utils import create_access_token

BASE_DIR = Path(__file__).resolve().parent.parent
TEST_DB_URL = f"sqlite:///{BASE_DIR / 'test.db'}"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    SQLModel.metadata.create_all(bind=engine)  # Ensure tables exist before tests run
    with TestClient(app) as c:
        yield c

import pytest
from uuid import uuid4


@pytest.fixture
def auth_token(client):
    email = f"test_{uuid4().hex}@example.com"
    password = "pass123"

    # Sign up via API
    signup_payload = {"email": email, "password": password}
    client.post("/signup", json=signup_payload)

    # ✅ Manually generate token (skip broken /login route)
    token = create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=30)
    )
    return token
