import requests
import json
import pycountry
import pandas as pd


api_key =f'013b31dd3339a724725d88524cfb37ba'





#url_gerne_list = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}'

#gerne_list = requests.get(url_gerne_list)
#if gerne_list.status_code == 200:
#    data_gerne_list = gerne_list.json()
    
#    print(data_gerne_list)



# list of all types of genres this api supports 
# {'genres': [{'id': 28, 'name': 'Action'}, {'id': 12, 'name': 'Adventure'}, {'id': 16, 'name': 'Animation'},
# {'id': 35, 'name': 'Comedy'}, {'id': 80, 'name': 'Crime'}, {'id': 99, 'name': 'Documentary'}, {'id': 18, 'name': 'Drama'}, 
# {'id': 10751, 'name': 'Family'}, {'id': 14, 'name': 'Fantasy'}, {'id': 36, 'name': 'History'}, {'id': 27, 'name': 'Horror'}, 
# {'id': 10402, 'name': 'Music'}, {'id': 9648, 'name': 'Mystery'}, {'id': 10749, 'name': 'Romance'}, {'id': 878, 'name': 'Science Fiction'}, 
# {'id': 10770, 'name': 'TV Movie'}, {'id': 53, 'name': 'Thriller'}, {'id': 10752, 'name': 'War'}, {'id': 37, 'name': 'Western'}]}

#put in genre id based on what the model predicts buy searching through the dictionary above
def Movie_info(genre_id):

    global api_key
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_id}&sort_by=popularity.desc"

    response1 = requests.get(url + "&page=1")
    data1 = response1.json()
    results = data1["results"]

    response2 = requests.get(url + "&page=2")
    data2 = response2.json()
    results.extend(data2["results"][:10]) 


    Movie_list = []

    Movie_actors =[]
    Movie_crew = []
    for i, movie in enumerate(results[:30], start=1):
        movie_details = {
            "title": movie["title"],
            "overview": movie["overview"],
            "release_date": movie["release_date"],
            "original_language": movie["original_language"],
            "poster_path": movie["poster_path"]

        }
        Movie_list.append(movie_details)

        # Append the dictionary to the Movie_list
        movie_id = movie['id']
        credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
        credits_response = requests.get(credits_url).json()

        # Extract top 3 actors
        for actor in credits_response['cast'][:5]:  # Limit to top 5 actors
            actor_data = {
                "movie_id": movie["id"],
                "movie_title": movie["title"],
                "actor_name": actor["name"],
                "character_name": actor["character"],
                "profile_path": f"https://image.tmdb.org/t/p/w500{actor['profile_path']}" if actor["profile_path"] else None
            }
            Movie_actors.append(actor_data)

        for crew_member in credits_response['crew']:
            if crew_member['job'] in ["Director"]: #, "Writer", "Cinematographer" can add writer and cinematogrpaher but some movies dont have so
                crew_data = {
                    "movie_id": movie["id"],
                    "movie_title": movie["title"],
                    "crew_name": crew_member["name"],
                    "job": crew_member["job"],
                    "profile_path": f"https://image.tmdb.org/t/p/w500{crew_member['profile_path']}" if crew_member["profile_path"] else None
                }
                Movie_crew.append(crew_data)
    return Movie_list,Movie_actors,Movie_crew


#Movies includes the title of the movie and a summary and relase date and the original language plus the poster_path whihc you can use to get the image of the movie for website use
#actors include the movie_id and movie title then name of a acotr in that movie and the charater name they played plus profile path each row is an actor so there will be multiple rows with the same movei as I got the top 5 actors in that movie
#crew includes the movie_id and movie title and the director of that movie can add like writer and chinetographer but some movies dont have so I didnt include for now


#the below converst to a pd dataframe so you can see the head and see hwo it is formatted
Movies,actors, crew = Movie_info(28)
movie_df = pd.DataFrame(Movies)
actors_df = pd.DataFrame(actors)

crew_df = pd.DataFrame(crew)
print(movie_df.head())
print(actors_df.head())
print(crew_df.head())


