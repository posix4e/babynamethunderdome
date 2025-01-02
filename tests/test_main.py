from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database import cleanup_db, init_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Reset database before each test"""
    cleanup_db()
    init_db()
    yield
    cleanup_db()


def test_create_session():
    response = client.post("/create-session")
    assert response.status_code == 200
    assert "session_id" in response.json()


def test_add_name():
    # Create a session first
    session_response = client.post("/create-session")
    session_id = session_response.json()["session_id"]

    # Add a name
    response = client.post(f"/add-name/{session_id}", data={"name": "Alice"})
    assert response.status_code == 200
    assert response.json()["success"] is True

    # Verify name was added
    names_response = client.get(f"/names/{session_id}")
    assert names_response.status_code == 200
    names = names_response.json()["names"]
    assert len(names) == 1
    assert names[0]["name"] == "Alice"
    assert names[0]["votes"] == 0


def test_compare_vote():
    # Create a session and add a name
    session_response = client.post("/create-session")
    session_id = session_response.json()["session_id"]
    client.post(f"/add-name/{session_id}", data={"name": "Bob"})

    # Vote for the name with voter info
    voter_info = {"name": "John", "age": 30}
    response = client.post(f"/compare-vote/{session_id}/Bob", json=voter_info)
    assert response.status_code == 200
    assert response.json()["success"] is True

    # Verify vote was counted
    names_response = client.get(f"/names/{session_id}")
    names = names_response.json()["names"]
    assert names[0]["name"] == "Bob"
    assert names[0]["votes"] == 1
    assert len(names[0]["voters"]) == 1
    assert names[0]["voters"][0]["voter_name"] == "John"
    assert names[0]["voters"][0]["voter_age"] == 30


def test_get_comparison():
    # Create a session and add two names
    session_response = client.post("/create-session")
    session_id = session_response.json()["session_id"]
    client.post(f"/add-name/{session_id}", data={"name": "Alice"})
    client.post(f"/add-name/{session_id}", data={"name": "Bob"})

    # Get comparison
    response = client.get(f"/get-comparison/{session_id}")
    assert response.status_code == 200
    names = response.json()["names"]
    assert len(names) == 2
    assert set(names) == {"Alice", "Bob"}

    # Vote for one name
    voter_info = {"name": "John", "age": 30}
    client.post(f"/compare-vote/{session_id}/{names[0]}", json=voter_info)

    # Get comparison again - should return error as all pairs compared
    response = client.get(f"/get-comparison/{session_id}")
    assert response.status_code == 200
    assert "error" in response.json()
    assert response.json()["error"] == "All pairs have been compared"
