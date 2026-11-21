"""
Pytest fixtures for E2E tests.
"""
import os
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def reset_database():
    """
    Reset database before each test.
    This ensures tests are independent.
    """
    # Remove test database if it exists
    test_db = "test_expenses.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Set environment variable so app uses test database
    os.environ["DATABASE_URL"] = test_db
    
    yield
    
    # Cleanup after test
    if os.path.exists(test_db):
        os.remove(test_db)


@pytest.fixture
def client():
    """
    Test client for the API.
    Each test gets a fresh client with clean database.
    """
    # Import here to pick up DATABASE_URL env var
    from app.main import app
    return TestClient(app)
