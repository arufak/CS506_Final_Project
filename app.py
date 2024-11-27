from flask import Flask, render_template, jsonify, request
import numpy as np
import matplotlib
import requests
import pycountry

app = Flask(__name__)

api_key_weather = 'aef5b02291330e9c41692e83d46e6c73'
api_key_movie = '013b31dd3339a724725d88524cfb37ba'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    country_name = "United States"
    country = pycountry.countries.get(name=country_name)
    country_code = country.alpha_2
    zip_code = '02215'

    url_location = f'http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={api_key_weather}'
    response_location = requests.get(url_location)
    if response_location.status_code == 200:
        data_location = response_location.json()
        latitude = data_location["lat"]
        longitude = data_location["lon"]

        url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key_weather}&units=imperial'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({'error': 'Failed to fetch weather data'}), response.status_code
    else:
        return jsonify({'error': 'Failed to fetch location data'}), response_location.status_code

@app.route('/hourly-weather')
def get_hourly_weather():
    country_name = "United States"
    country = pycountry.countries.get(name=country_name)
    country_code = country.alpha_2
    zip_code = '02134'

    url_location = f'http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={api_key_weather}'
    response_location = requests.get(url_location)
    if response_location.status_code == 200:
        data_location = response_location.json()
        latitude = data_location["lat"]
        longitude = data_location["lon"]

        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key_weather}&units=imperial'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({'error': 'Failed to fetch hourly weather data'}), response.status_code
    else:
        return jsonify({'error': 'Failed to fetch location data'}), response_location.status_code

def get_movies_by_genre(genre_id):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key_movie}&with_genres={genre_id}&sort_by=popularity.desc"
    response1 = requests.get(url + "&page=1")
    data1 = response1.json()
    results = data1["results"]

    response2 = requests.get(url + "&page=2")
    data2 = response2.json()
    results.extend(data2["results"][:10])

    movies = []
    for movie in results[:30]:
        movie_details = {
            "title": movie["title"],
            "overview": movie["overview"],
            "release_date": movie["release_date"],
            "original_language": movie["original_language"],
            "poster_path": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie["poster_path"] else None
        }
        movies.append(movie_details)
    return movies

def get_movie_details(title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key_movie}&query={title}"
    search_response = requests.get(search_url)
    if search_response.status_code == 200:
        search_data = search_response.json()
        if search_data["results"]:
            movie_id = search_data["results"][0]["id"]
            credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key_movie}"
            credits_response = requests.get(credits_url)
            if credits_response.status_code == 200:
                credits_data = credits_response.json()
                actors = [{"name": actor["name"]} for actor in credits_data["cast"][:5]]
                director = next((member for member in credits_data["crew"] if member["job"] == "Director"), None)
                return {"actors": actors, "director": {"name": director["name"]} if director else None}
    return {"actors": [], "director": None}

@app.route('/genres')
def get_genres():
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key_movie}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return jsonify(data['genres'])
    else:
        return jsonify({'error': 'Failed to fetch genres'}), response.status_code

@app.route('/movies')
def movies():
    genre = request.args.get('genre')
    genres_response = requests.get(f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key_movie}&language=en-US")
    if genres_response.status_code == 200:
        genres_data = genres_response.json()
        genre_map = {g['name'].lower(): g['id'] for g in genres_data['genres']}
        genre_id = genre_map.get(genre.lower())
        if genre_id:
            movies = get_movies_by_genre(genre_id)
            return jsonify(movies)
        else:
            return jsonify({'error': 'Invalid genre'}), 400
    else:
        return jsonify({'error': 'Failed to fetch genres'}), genres_response.status_code

@app.route('/movie-details')
def movie_details():
    title = request.args.get('title')
    if title:
        details = get_movie_details(title)
        return jsonify(details)
    else:
        return jsonify({'error': 'Title not provided'}), 400
    
if __name__ == "__main__":
    app.run(debug=True)
