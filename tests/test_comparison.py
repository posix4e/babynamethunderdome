from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_name_comparison_flow():
    # Create a new session
    response = client.post("/create-session")
    assert response.status_code == 200
    session_id = response.json()["session_id"]

    # Add two names
    response = client.post(f"/add-name/{session_id}", data={"name": "Alice"})
    assert response.status_code == 200
    response = client.post(f"/add-name/{session_id}", data={"name": "Bob"})
    assert response.status_code == 200

    # Get a comparison
    response = client.get(f"/get-comparison/{session_id}")
    assert response.status_code == 200
    comparison = response.json()
    assert len(comparison["names"]) == 2
    assert set(comparison["names"]) == {"Alice", "Bob"}

    # Submit a vote with voter info
    voter_info = {"name": "John", "age": 30}
    response = client.post(f"/compare-vote/{session_id}/Alice", json=voter_info)
    assert response.status_code == 200

    # Check that the vote was recorded
    response = client.get(f"/names/{session_id}")
    assert response.status_code == 200
    names = response.json()["names"]
    
    alice_votes = next(n for n in names if n["name"] == "Alice")
    assert len(alice_votes["voters"]) == 1
    assert alice_votes["voters"][0]["voter_name"] == "John"
    assert alice_votes["voters"][0]["voter_age"] == 30

    # Try to get another comparison - should be none left
    response = client.get(f"/get-comparison/{session_id}")
    assert response.status_code == 200
    assert "error" in response.json()
    assert response.json()["error"] == "All pairs have been compared"
