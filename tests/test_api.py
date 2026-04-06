import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models.user import User
from app.models.record import Record
from app.services.user_service import create_user
from app.services.record_service import create_record
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.schemas.record import RecordCreate

client = TestClient(app)

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200

def test_summary_viewer(client):
    headers = {"X-User-Role": "viewer"}
    response = client.get("/api/v1/records/summary/", headers=headers)
    assert response.status_code == 200

def test_summary_analyst(client):
    headers = {"X-User-Role": "analyst", "X-User-ID": "1"}
    response = client.get("/api/v1/records/summary/", headers=headers)
    assert response.status_code == 200

def test_records_analyst(client):
    headers = {"X-User-Role": "analyst"}
    response = client.get("/api/v1/records/", headers=headers)
    assert response.status_code == 200

def test_records_viewer(client):
    headers = {"X-User-Role": "viewer"}
    response = client.get("/api/v1/records/", headers=headers)
    assert response.status_code == 403  # insufficient role

def test_records_no_role(client):
    response = client.get("/api/v1/records/")
    assert response.status_code == 401

def test_record_create_admin(db: Session):
    user_data = UserCreate(email="test@example.com", role="admin")
    user = create_user(db=db, user=user_data)
    record_data = RecordCreate(amount=100.0, type="income", category="Salary", date="2024-01-01")
    record = create_record(db=db, record=record_data, user_id=user.id)
    assert record is not None

# Add more tests for errors, roles, search etc.

def test_invalid_role(client):
    headers = {"X-User-Role": "hacker"}
    response = client.get("/api/v1/records/summary/", headers=headers)
    assert response.status_code == 401
