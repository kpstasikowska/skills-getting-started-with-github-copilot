import copy

from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def setup_function():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(app_module.INITIAL_ACTIVITIES))


def test_unregister_participant_removes_email_from_activity():
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Removed michael@mergington.edu from Chess Club"
    }

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_participant_returns_404_for_unknown_activity():
    response = client.delete("/activities/Unknown Activity/participants/student@mergington.edu")

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_rejects_duplicate_participant():
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up for this activity"}
