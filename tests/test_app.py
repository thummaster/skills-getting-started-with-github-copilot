import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

ACTIVITY = "Chess Club"
EMAIL = "testuser@mergington.edu"


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert ACTIVITY in data
    assert "participants" in data[ACTIVITY]


def test_signup_for_activity():
    # Remove if already present
    client.post(f"/activities/{ACTIVITY}/unregister?email={EMAIL}")
    response = client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    assert response.status_code == 200
    data = response.json()
    assert f"Signed up {EMAIL}" in data["message"]
    # Try duplicate signup
    response_dup = client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    assert response_dup.status_code == 400


def test_unregister_from_activity():
    # Ensure user is signed up
    client.post(f"/activities/{ACTIVITY}/signup?email={EMAIL}")
    response = client.post(f"/activities/{ACTIVITY}/unregister?email={EMAIL}")
    assert response.status_code == 200
    data = response.json()
    assert f"Unregistered {EMAIL}" in data["message"]
    # Try duplicate unregister
    response_dup = client.post(f"/activities/{ACTIVITY}/unregister?email={EMAIL}")
    assert response_dup.status_code == 404
