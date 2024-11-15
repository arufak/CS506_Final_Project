import pandas as pd
import requests

# TMDb API key
api_key = f'013b31dd3339a724725d88524cfb37ba'

def add_movies_by_keyword_to_dataset(keyword, current_df=None, weather_type=""):
    # Define the list of all weather columns
    weather_columns = ["Clear Sky", "Few Clouds", "Scattered Clouds", "Broken Clouds",
                       "Shower Rain", "Rain", "Thunderstorm", "Snow", "Mist"]
    
    # Initialize the dataset if it's None
    if current_df is None:
        current_df = pd.DataFrame(columns=[
            "title", "original_title", "overview", "release_date", "runtime", 
            "genres", "status", "original_language", "tagline", "popularity", 
            "vote_average", "vote_count", "cast", "director", "producer", 
            "cinematographer", "poster", "keywords", "production_companies", 
            "production_countries", "budget", "revenue"
        ] + weather_columns)
    
    # Step 1: Search for the keyword to get the keyword ID
    keyword_url = f'https://api.themoviedb.org/3/search/keyword?api_key={api_key}&query={keyword}'
    keyword_response = requests.get(keyword_url).json()
    
    # Check if the keyword exists
    if not keyword_response['results']:
        print(f"No results found for keyword '{keyword}'.")
        return current_df
    
    keyword_id = keyword_response['results'][0]['id']
    print(f"Found keyword '{keyword}' with ID: {keyword_id}")
    
    # Step 2: Use the keyword ID to get associated movies
    movie_url = f'https://api.themoviedb.org/3/keyword/{keyword_id}/movies?api_key={api_key}'
    movie_response = requests.get(movie_url).json()
    movies = movie_response['results']
    
    # Step 3: Fetch detailed information for each movie and structure the data
    movie_data = []
    for movie in movies:
        # Get movie details
        movie_id = movie['id']
        details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits,keywords,images,videos'
        details_response = requests.get(details_url).json()
        
        # Extract required fields
        movie_info = {
            "title": details_response.get("title"),
            "original_title": details_response.get("original_title"),
            "overview": details_response.get("overview", "No overview available"),
            "release_date": details_response.get("release_date", "No release date"),
            "runtime": details_response.get("runtime"),
            "genres": [genre["name"] for genre in details_response.get("genres", [])],
            "status": details_response.get("status"),
            "original_language": details_response.get("original_language"),
            "tagline": details_response.get("tagline"),
            "popularity": details_response.get("popularity"),
            "vote_average": details_response.get("vote_average"),
            "vote_count": details_response.get("vote_count"),
            "production_companies": [company["name"] for company in details_response.get("production_companies", [])],
            "production_countries": [country["name"] for country in details_response.get("production_countries", [])],
            "budget": details_response.get("budget"),
            "revenue": details_response.get("revenue"),
            "poster": f"https://image.tmdb.org/t/p/w500{details_response.get('poster_path')}" if details_response.get("poster_path") else None,
            "keywords": [keyword["name"] for keyword in details_response.get("keywords", {}).get("keywords", [])]
        }
        
        # Process cast: Get top 3 actors with real name and character name
        cast = details_response.get("credits", {}).get("cast", [])
        top_cast = [{"name": member["name"], "character": member["character"]} for member in cast[:3]]
        movie_info["cast"] = top_cast
        
        # Process crew: Only director, producer, and cinematographer
        crew = details_response.get("credits", {}).get("crew", [])
        for member in crew:
            if member["job"] == "Director":
                movie_info["director"] = member["name"]
            elif member["job"] == "Producer":
                movie_info["producer"] = member["name"]
            elif member["job"] == "Director of Photography":
                movie_info["cinematographer"] = member["name"]

        # Set weather type columns: 1 for the specified weather, 0 for others
        for weather in weather_columns:
            movie_info[weather] = 1 if weather == weather_type else 0

        # Append the movie info to movie_data list
        movie_data.append(movie_info)
    
    # Convert movie_data list to a DataFrame
    new_movies_df = pd.DataFrame(movie_data)
    
    # Step 4: Append to the existing dataset (empty or not)
    updated_df = pd.concat([current_df, new_movies_df], ignore_index=True)
    print(f"Added {len(new_movies_df)} movies with keyword '{keyword}' under weather type '{weather_type}'.")
    
    return updated_df

# Example usage with an empty dataset
# Define the mapping of weather types to their top moods/emotions (keywords)
weather_keywords = {
    "Clear Sky": ["Uplifting", "Light-hearted", "Inspirational", "Joyful", "Adventurous"],
    "Few Clouds": ["Playful", "Relaxed", "Nostalgic", "Romantic", "Warm"],
    "Scattered Clouds": ["Reflective", "Curious", "Intense", "Melancholic", "Thoughtful"],
    "Broken Clouds": ["Mysterious", "Suspenseful", "Reflective", "Dark", "Intense"],
    "Shower Rain": ["Cozy", "Introspective", "Emotional", "Comforting", "Reflective"],
    "Rain": ["Nostalgic", "Melancholic", "Reflective", "Introspective", "Calm"],
    "Thunderstorm": ["Suspenseful", "Exciting", "Dark", "Adventurous", "Intense"],
    "Snow": ["Cozy", "Nostalgic", "Introspective", "Comforting", "Reflective"],
    "Mist": ["Mysterious", "Suspenseful", "Dark", "Eerie", "Thought-provoking"]
}

# Initialize an empty DataFrame to start (or use an existing one if available)
current_df = None

# Loop through each weather type and its keywords
for weather_type, keywords in weather_keywords.items():
    print(f"Processing weather type: {weather_type}")
    
    # For each keyword associated with the weather type, call the function
    for keyword in keywords:
        print(f"Searching for movies with keyword: '{keyword}' under weather type '{weather_type}'")
        
        # Call the function and update the dataset with movies associated with each keyword
        current_df = add_movies_by_keyword_to_dataset(keyword, current_df, weather_type)
        print("\nCurrent dataset head:")
        print(current_df.head())
        
        print("\nCurrent dataset info:")
        print(current_df.info())

# Display the resulting dataset
print("Final dataset:")
print(current_df.head())

# Optionally, save the final dataset to a CSV file
current_df.to_csv("movies_with_weather_associations.csv", index=False)
