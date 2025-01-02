import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# Set test environment
os.environ['TESTING'] = 'true'

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    # Create test database tables
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Drop test database tables
    Base.metadata.drop_all(bind=engine)

def test_create_session(client):
    response = client.post("/create-session")
    assert response.status_code == 200
    assert "session_id" in response.json()

def test_add_name(client):
    # Create session first
    session_response = client.post("/create-session")
    session_id = session_response.json()["session_id"]
    
    # Add name
    response = client.post(
        f"/add-name/{session_id}",
        data={"name": "TestName"}
    )
    assert response.status_code == 200
    assert response.json()["success"] is True

    # Verify name was added
    names_response = client.get(f"/names/{session_id}")
    assert names_response.status_code == 200
    names = names_response.json()["names"]
    assert len(names) == 1
    assert names[0]["name"] == "TestName"
    assert names[0]["votes"] == 0

def test_compare_vote(client):
    # Create session
    session_response = client.post("/create-session")
    session_id = session_response.json()["session_id"]
    
    # Add two names
    client.post(f"/add-name/{session_id}", data={"name": "Name1"})
    client.post(f"/add-name/{session_id}", data={"name": "Name2"})
    
    # Get comparison
    comparison_response = client.get(f"/get-comparison/{session_id}")
    assert comparison_response.status_code == 200
    names = comparison_response.json()["names"]
    assert len(names) == 2
    
    # Vote for first name
    name_to_vote = names[0]
    vote_response = client.post(
        f"/compare-vote/{session_id}/{name_to_vote}",
        json={"name": "Voter1", "age": 25}
    )
    assert vote_response.status_code == 200
    assert vote_response.json()["success"] is True
    
    # Verify vote was counted
    names_response = client.get(f"/names/{session_id}")
    names = names_response.json()["names"]
    voted_name = next(n for n in names if n["name"] == name_to_vote)
    assert voted_name["votes"] == 1
    assert voted_name["voters"][0]["voter_name"] == "Voter1"
    assert voted_name["voters"][0]["voter_age"] == 25
