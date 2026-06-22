"""Unit tests for the CI/CD lab Flask application."""

import os

import pytest
from src.app import app as flask_app


@pytest.fixture
def client():
    """Create a Flask test client.

    Yields:
        FlaskClient: The test client instance.
    """
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


class TestIndex:
    """Tests for the / endpoint."""

    def test_index_returns_200(self, client):
        """GET / should return HTTP 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_index_contains_service_field(self, client):
        """GET / response must include 'service' key."""
        response = client.get("/")
        data = response.get_json()
        assert "service" in data
        assert data["service"] == "devops-cicd-lab"

    def test_index_contains_version(self, client):
        """GET / response must include 'version' key."""
        data = client.get("/").get_json()
        assert "version" in data

    def test_index_contains_hostname(self, client):
        """GET / response must include 'hostname' key."""
        data = client.get("/").get_json()
        assert "hostname" in data


class TestHealth:
    """Tests for the /health endpoint."""

    def test_health_returns_200(self, client):
        """GET /health should return HTTP 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_status_ok(self, client):
        """GET /health should return {status: ok}."""
        data = client.get("/health").get_json()
        assert data == {"status": "ok"}

    def test_health_is_json(self, client):
        """GET /health response Content-Type must be application/json."""
        response = client.get("/health")
        assert "application/json" in response.content_type


class TestGreeting:
    """Tests for the /greeting endpoint with feature flag."""

    def test_greeting_default(self, client):
        """Without feature flag /greeting returns classic message."""
        os.environ.pop("FEATURE_NEW_GREETING", None)
        data = client.get("/greeting").get_json()
        assert data["greeting"] == "Hello, World!"

    def test_greeting_new_feature_enabled(self, client):
        """With FEATURE_NEW_GREETING=true /greeting returns new message."""
        os.environ["FEATURE_NEW_GREETING"] = "true"
        try:
            data = client.get("/greeting").get_json()
            assert "new greeting" in data["greeting"].lower()
        finally:
            os.environ.pop("FEATURE_NEW_GREETING", None)

    def test_greeting_feature_disabled(self, client):
        """With FEATURE_NEW_GREETING=false /greeting returns classic message."""
        os.environ["FEATURE_NEW_GREETING"] = "false"
        try:
            data = client.get("/greeting").get_json()
            assert data["greeting"] == "Hello, World!"
        finally:
            os.environ.pop("FEATURE_NEW_GREETING", None)

    def test_greeting_returns_200(self, client):
        """GET /greeting should always return HTTP 200."""
        response = client.get("/greeting")
        assert response.status_code == 200
