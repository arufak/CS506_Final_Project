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
    assert b"<title>" in response.data  # Check if the response contains HTML content.

def test_get_weather(client):
    """Test the weather API."""
    response = client.get('/weather')
    assert response.status_code == 200
    assert 'weather' in response.json  # Ensure weather data is returned.

def test_invalid_weather_route(client):
    """Test invalid weather data."""
    response = client.get('/weather?zip=99999')  # Invalid ZIP code
    assert response.status_code != 200

def test_get_movies(client):
    """Test the movies API."""
    response = client.get('/movies?genre=Action')
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Ensure a list of movies is returned.

def test_invalid_movie_genre(client):
    """Test invalid genre for movies."""
    response = client.get('/movies?genre=InvalidGenre')
    assert response.status_code == 400  # Invalid genre should return a 400 error.

def test_recommended_movies(client):
    """Test the recommended movies API."""
    response = client.get('/recommended-movies')
    assert response.status_code == 200
    assert 'genres' in response.json
    assert 'movies_by_genre' in response.json
    assert 'suggested_movies' in response.json
