"""
Test configuration and fixtures for FastAPI application tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_activity():
    """Sample activity data for testing."""
    return {
        "name": "Test Club",
        "description": "A test club for testing purposes",
        "schedule": "Mondays, 3:00 PM - 4:00 PM",
        "max_participants": 10,
        "participants": ["test1@mergington.edu", "test2@mergington.edu"]
    }


@pytest.fixture
def valid_email():
    """Valid email for testing."""
    return "student@mergington.edu"


@pytest.fixture
def invalid_email():
    """Invalid email for testing."""
    return "invalid-email"