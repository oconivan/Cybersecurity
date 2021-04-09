import requests

#function to get movie requests
def getMovie(key, movie_name):
    parameters = {'s':movie_name, 'type':'movie'}
    result = requests.get(key, parameters)
    return eval(result.content.decode('utf-8'))