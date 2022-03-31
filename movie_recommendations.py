# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
import requests_with_caching
import requests
import json

def get_movies_from_tastedive(q, lim = 5, typ = 'movies'):
    #https://tastedive.com/read/api for documentation on this API
    baseurl = 'https://tastedive.com/api/similar'
    params = {}
    params['q'] = q
    params['limit'] = lim
    params['type'] = typ
    get_movies_resp = requests_with_caching.get(baseurl, params)
    print(get_movies_resp.url) # Paste the result into the browser to check it out...
    return get_movies_resp.json()

def extract_movie_titles(dictionary):
    movie_titles = [x['Name'] for x in dictionary['Similar']['Results']]
    return movie_titles

def get_related_titles(movie_titles):
    related_titles = []
    temp_titles = []
    temp_titles = [extract_movie_titles(get_movies_from_tastedive(x)) for x in movie_titles]
    for x in temp_titles:
        for y in x:
            if y not in related_titles:
                related_titles.append(y)
    return related_titles

def get_movie_data(movie_title):
    #for external retrieval must include APIkey: http://www.omdbapi.com/
    # https://www.omdbapi.com for documentation on this API
    baseurl = 'http://www.omdbapi.com/'
    params = {}
    params['t'] = movie_title
    params['r'] = 'json'
    get_movie_resp = requests_with_caching.get(baseurl, params)
    print(get_movie_resp.url)
    return get_movie_resp.json()

def get_movie_rating(movie_dict):
    print(movie_dict['Ratings'])
    rating = 0
    ratings = []
    ratings = [x['Value'] for x in movie_dict['Ratings'] if x['Source'] == 'Rotten Tomatoes']
    if len(ratings) != 0:
        rating = int(ratings[0][:2])
    return rating

def get_sorted_recommendations(movie_titles):
    #related_movies = []
    related_movies = get_related_titles(movie_titles)
    related_movies = sorted(related_movies, key = lambda x: (get_movie_rating(get_movie_data(x)),x), reverse = True)
    #print(related_movies)
    return related_movies
  
