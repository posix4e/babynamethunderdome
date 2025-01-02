import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, cleanup_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    init_db()
    yield
    cleanup_db()

def test_vote_page_contains_share_button():
    # Create a test session
    response = client.post('/create-session')
    assert response.status_code == 200
    session_id = response.json()['session_id']
    
    # Get the vote page
    response = client.get(f'/vote-page?session={session_id}')
    assert response.status_code == 200
    
    # Check if the share button exists in the HTML
    assert 'id="share-button"' in response.text
    assert 'shareVotingLink()' in response.text
    
def test_vote_page_contains_share_api_code():
    # Create a test session
    response = client.post('/create-session')
    assert response.status_code == 200
    session_id = response.json()['session_id']
    
    # Get the vote page
    response = client.get(f'/vote-page?session={session_id}')
    assert response.status_code == 200
    
    # Check if the share API code exists in the HTML
    html_content = response.text
    assert 'navigator.share' in html_content
    assert 'shareTitle' in html_content
    assert 'shareText' in html_content
    assert 'shareUrl' in html_content
