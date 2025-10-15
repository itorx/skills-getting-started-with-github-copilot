import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Ensure user is not already signed up
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    assert "already signed up" in response_dup.json()["detail"]


def test_unregister_from_activity():
    email = "testuser2@mergington.edu"
    activity = "Programming Class"
    # Sign up first
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]
    # Try to unregister again (should fail)
    response_fail = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_fail.status_code == 404
    assert "Participant not found" in response_fail.json()["detail"]


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_activity_not_found():
    response = client.post("/activities/Nonexistent/unregister?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
