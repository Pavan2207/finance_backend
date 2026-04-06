import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_viewer_summary():
    response = client.get("/api/v1/records/summary/", headers={"X-User-Role": "viewer"})
    assert response.status_code == 200

def test_analyst_records():
    response = client.get("/api/v1/records/", headers={"X-User-Role": "analyst"})
    assert response.status_code == 200

def test_admin_user_create():
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@test.com", "role": "viewer"},
        headers={"X-User-Role": "admin"}
    )
    assert response.status_code == 200

def test_admin_invalid():
    response = client.post("/api/v1/users/", headers={"X-User-Role": "viewer"})
    assert response.status_code == 403

def test_record_crud():
    # Create
    create_resp = client.post(
        "/api/v1/records/",
        json={"amount": 1000, "type": "income", "category": "Salary", "date": "2026-04-06"},
        headers={"X-User-Role": "admin", "X-User-ID": 1}
    )
    assert create_resp.status_code == 200
    record_id = create_resp.json()["id"]
    
    # Read
    get_resp = client.get(f"/api/v1/records/{record_id}", headers={"X-User-Role": "admin"})
    assert get_resp.status_code == 200
    
    # Update
    update_resp = client.put(f"/api/v1/records/{record_id}", json={"amount": 2000}, headers={"X-User-Role": "admin"})
    assert update_resp.status_code == 200
    
    # Delete
    del_resp = client.delete(f"/api/v1/records/{record_id}", headers={"X-User-Role": "admin"})
    assert del_resp.status_code == 204

def test_filter_pagination():
    response = client.get("/api/v1/records/?type=income&limit=5", headers={"X-User-Role": "admin"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5

def test_trends():
    response = client.get("/api/v1/records/trends/?period=monthly", headers={"X-User-Role": "viewer"})
    assert response.status_code == 200

