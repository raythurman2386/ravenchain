import pytest
from fastapi.testclient import TestClient
from api.main import app

def test_health_endpoint():
    """Test health endpoint"""
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
