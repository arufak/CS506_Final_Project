import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the homepage route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"<title>" in response.data  # Check for HTML content in the response

def test_weather_api(client):
    """Test the weather API endpoint."""
    response = client.get('/weather')
    assert response.status_code == 200
    assert 'weather' in response.json or 'error' in response.json  # Verify weather data or error handling

def test_movies_by_genre(client):
    """Test the movies API with a valid genre."""
    response = client.get('/movies?genre=Action')
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Should return a list of movies

def test_invalid_genre(client):
    """Test the movies API with an invalid genre."""
    response = client.get('/movies?genre=InvalidGenre')
    assert response.status_code == 400  # Invalid genre should return a 400 error

def test_recommended_movies(client):
    """Test the recommended movies API."""
    response = client.get('/recommended-movies')
    assert response.status_code == 200
    assert 'genres' in response.json
    assert 'movies_by_genre' in response.json
    assert 'suggested_movies' in response.json


