from flask import Flask, render_template, jsonify, request, send_from_directory
import pandas as pd
import requests
import gzip

app = Flask(__name__)

api_key_weather = 'aef5b02291330e9c41692e83d46e6c73'
api_key_movie = '013b31dd3339a724725d88524cfb37ba'

# Load the compressed CSV file with the correct encoding
with gzip.open('data/data_weather_mapped.csv.gz', 'rt', encoding='utf-8') as f:
    df = pd.read_csv(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    country_code = "US"
    zip_code = '02215'  # Default ZIP code; replace if a query parameter is provided

    if 'zip' in request.args:
        zip_code = request.args.get('zip')

    url_location = f'http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={api_key_weather}'
    response_location = requests.get(url_location)
    if response_location.status_code == 200:
        data_location = response_location.json()
        if "lat" in data_location and "lon" in data_location:  # Ensure valid location data
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
            return jsonify({'error': 'Invalid ZIP code'}), 400
    else:
        return jsonify({'error': 'Failed to fetch location data'}), response_location.status_code


@app.route('/hourly-weather')
def get_hourly_weather():
    country_code = "US"
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
            movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key_movie}"
            movie_details_response = requests.get(movie_details_url)
            if movie_details_response.status_code == 200:
                movie_details_data = movie_details_response.json()
                release_year = movie_details_data.get("release_date", "").split("-")[0]
                tagline = movie_details_data.get("tagline", "")
                genres = [genre["name"] for genre in movie_details_data.get("genres", [])]
                credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key_movie}"
                credits_response = requests.get(credits_url)
                if credits_response.status_code == 200:
                    credits_data = credits_response.json()
                    actors = [{"name": actor["name"]} for actor in credits_data["cast"][:5]]
                    director = next((member for member in credits_data["crew"] if member["job"] == "Director"), None)
                    return {
                        "release_year": release_year,
                        "tagline": tagline,
                        "genres": genres,
                        "actors": actors,
                        "director": {"name": director["name"]} if director else None
                    }
    return {"release_year": None, "tagline": "", "genres": [], "actors": [], "director": None}

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

def get_current_weather():
    country_code = "US"
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
            return data['weather'][0]['main']  # Return the main weather condition
        else:
            return None
    else:
        return None

def get_movies_by_weather(weather):
    filtered_df = df[df['Weather'].str.contains(weather, case=False, na=False)]
    filtered_df = filtered_df[filtered_df['poster'].notna() & (filtered_df['poster'] != '')]  # Filter out rows where 'poster' is NaN or empty
    return filtered_df

def get_popular_genres(filtered_df):
    genres_series = filtered_df['genres'].str.strip("[]").str.replace("'", "").str.split(', ')
    genres = genres_series.explode().value_counts().index.tolist()
    return genres[:5]  # Return the top 5 genres

@app.route('/recommended-movies')
def recommended_movies():
    weather = get_current_weather()
    if weather:
        filtered_df = get_movies_by_weather(weather)
        popular_genres = get_popular_genres(filtered_df)

        # Get movies for the popular genres
        genre_movies = {}
        added_movies = set()  # Keep track of added movies

        for genre in popular_genres:
            genre_movies[genre] = []
            genre_df = filtered_df[filtered_df['genres'].str.contains(genre, case=False, na=False)]
            for _, movie in genre_df.iterrows():
                if movie['title'] not in added_movies:
                    genre_movies[genre].append(movie.to_dict())
                    added_movies.add(movie['title'])

        # Handle NaN values before converting to JSON
        for genre, movies in genre_movies.items():
            for movie in movies:
                for key, value in movie.items():
                    if pd.isna(value):
                        movie[key] = None

        # Handle NaN values in suggested movies
        suggested_movies = filtered_df.sample(n=30, random_state=1).to_dict('records')
        for movie in suggested_movies:
            for key, value in movie.items():
                if pd.isna(value):
                    movie[key] = None

        # Sort suggested movies by popularity
        suggested_movies.sort(key=lambda x: x.get('popularity', 0), reverse=True)

        return jsonify({
            'genres': popular_genres,
            'movies_by_genre': genre_movies,
            'suggested_movies': suggested_movies
        })
    else:
        return jsonify({'error': 'Failed to fetch current weather'}), 500
    
@app.route('/load-html/<filename>')
def load_html(filename):
    return send_from_directory('html', filename)

if __name__ == "__main__":
    app.run(debug=True)
