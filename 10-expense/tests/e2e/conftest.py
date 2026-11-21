"""
Pytest fixtures for E2E tests.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """
    Test client for the API.
    Each test gets a fresh client.
    """
    return TestClient(app)


# TODO: Add fixture to reset database between tests
# when database is implemented
