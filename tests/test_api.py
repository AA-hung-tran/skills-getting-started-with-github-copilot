"""
Tests for the FastAPI application endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


class TestAPI:
    """Test class for API endpoints."""

    def setup_method(self):
        """Reset activities data before each test."""
        # Reset to original test data
        activities.clear()
        activities.update({
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
            }
        })

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return TestClient(app)

    def test_root_redirect(self, client):
        """Test that root serves the HTML page (after redirect)."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Mergington High School" in response.text

    def test_get_activities(self, client):
        """Test getting all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        
        chess_club = data["Chess Club"]
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["max_participants"] == 12
        assert len(chess_club["participants"]) == 2

    def test_signup_success(self, client):
        """Test successful signup for an activity."""
        response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
        assert response.status_code == 200
        
        data = response.json()
        assert "Signed up newstudent@mergington.edu for Chess Club" in data["message"]
        
        # Verify the participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "newstudent@mergington.edu" in activities_data["Chess Club"]["participants"]

    def test_signup_duplicate_participant(self, client):
        """Test signup when student is already registered."""
        response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")
        assert response.status_code == 400
        
        data = response.json()
        assert "Student already signed up for this activity" in data["detail"]

    def test_signup_nonexistent_activity(self, client):
        """Test signup for a non-existent activity."""
        response = client.post("/activities/Nonexistent Club/signup?email=test@mergington.edu")
        assert response.status_code == 404
        
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_success(self, client):
        """Test successful unregistration from an activity."""
        response = client.delete("/activities/Chess Club/unregister?email=michael@mergington.edu")
        assert response.status_code == 200
        
        data = response.json()
        assert "Unregistered michael@mergington.edu from Chess Club" in data["message"]
        
        # Verify the participant was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "michael@mergington.edu" not in activities_data["Chess Club"]["participants"]

    def test_unregister_not_registered(self, client):
        """Test unregistration when student is not registered."""
        response = client.delete("/activities/Chess Club/unregister?email=notregistered@mergington.edu")
        assert response.status_code == 404
        
        data = response.json()
        assert "Student not registered for this activity" in data["detail"]

    def test_unregister_nonexistent_activity(self, client):
        """Test unregistration from a non-existent activity."""
        response = client.delete("/activities/Nonexistent Club/unregister?email=test@mergington.edu")
        assert response.status_code == 404
        
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_activity_capacity_tracking(self, client):
        """Test that activity capacity is properly tracked."""
        # Get initial state
        response = client.get("/activities")
        initial_data = response.json()
        initial_count = len(initial_data["Chess Club"]["participants"])
        
        # Add a participant
        client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
        
        # Verify count increased
        response = client.get("/activities")
        updated_data = response.json()
        updated_count = len(updated_data["Chess Club"]["participants"])
        assert updated_count == initial_count + 1
        
        # Remove a participant
        client.delete("/activities/Chess Club/unregister?email=newstudent@mergington.edu")
        
        # Verify count decreased
        response = client.get("/activities")
        final_data = response.json()
        final_count = len(final_data["Chess Club"]["participants"])
        assert final_count == initial_count

    def test_multiple_signups_and_removals(self, client):
        """Test multiple signup and removal operations."""
        emails = ["test1@mergington.edu", "test2@mergington.edu", "test3@mergington.edu"]
        
        # Sign up multiple students
        for email in emails:
            response = client.post(f"/activities/Programming Class/signup?email={email}")
            assert response.status_code == 200
        
        # Verify all were added
        response = client.get("/activities")
        data = response.json()
        participants = data["Programming Class"]["participants"]
        for email in emails:
            assert email in participants
        
        # Remove some students
        for email in emails[:2]:
            response = client.delete(f"/activities/Programming Class/unregister?email={email}")
            assert response.status_code == 200
        
        # Verify they were removed
        response = client.get("/activities")
        data = response.json()
        participants = data["Programming Class"]["participants"]
        assert emails[0] not in participants
        assert emails[1] not in participants
        assert emails[2] in participants

    def test_activity_data_structure(self, client):
        """Test that activities have the expected data structure."""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        for activity_name, activity_data in data.items():
            assert isinstance(activity_name, str)
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0