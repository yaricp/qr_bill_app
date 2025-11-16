import pytest
from fastapi.testclient import TestClient
from src.api import app


@pytest.fixture(scope="function")
def test_client():
    # Create test client that uses the app and DB session
    client = TestClient(app)
    return client


def test_get_metrics(test_client):
    """Test get metrics"""
    response = test_client.get("/metrics/")
    assert response.status_code == 200
