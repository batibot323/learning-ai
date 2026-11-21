"""
E2E test: Health check.

This is the only test that should pass with the skeleton.
"""


def test_health_check(client):
    """App should respond to health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
