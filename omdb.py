import os 
from dotenv import load_dotenv
import requests

load_dotenv()

def get_movie_info(movie_title):
    url = 'http://www.omdbapi.com'
    api_key = os.getenv('OMDB_API_KEY')
    data = {'apikey':api_key, 't':movie_title}
    response = requests.get(url, data).json()

    if response.get('Response') != 'True':
        return None

    movie_info = {}
    movie_info["title"] = response.get("Title")
    movie_info["poster"] = response.get("Poster")
    movie_info["genre"] = response.get("Genre")
    movie_info["year"] = response.get("Year")
    movie_info["plot"] = response.get("Plot")
    movie_info["actors"] = response.get("Actors")
    movie_info["ratings"] = response.get("Ratings")
    movie_info["director"] = response.get("Director")
    movie_info["runtime"] = response.get("Runtime")
    movie_info["imdb_rating"] = response.get("imdbRating")

    return movie_info
