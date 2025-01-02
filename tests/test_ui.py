from fastapi.testclient import TestClient
from bs4 import BeautifulSoup
from app.main import app

client = TestClient(app)

def test_vote_page_accessibility():
    response = client.get("/vote-page?session=test123")
    assert response.status_code == 200
    
    # Parse HTML to check for accessibility attributes
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check if voting options have proper accessibility attributes
    name_options = soup.find_all(class_="name-option")
    for option in name_options:
        assert option.get('role') == 'button'
        assert option.get('tabindex') == '0'
        assert 'onkeypress' in option.attrs

def test_index_page_sharing():
    response = client.get("/?session=test123")
    assert response.status_code == 200
    
    # Parse HTML to check for sharing elements
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check for copy buttons
    copy_buttons = soup.find_all(class_="copy-button")
    assert len(copy_buttons) == 2  # One for admin link, one for voting link
    
    # Check for share link containers
    share_links = soup.find_all(class_="share-link")
    assert len(share_links) == 2  # One for admin link, one for voting link

def test_vote_page_sharing():
    response = client.get("/vote-page?session=test123")
    assert response.status_code == 200
    
    # Parse HTML to check for sharing button
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check for share button
    share_button = soup.find(class_="share-button")
    assert share_button is not None
    assert "Share this comparison" in share_button.text
