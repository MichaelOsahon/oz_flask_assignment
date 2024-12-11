import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import requests
import urllib.request
import spotipy.util as util
from datetime import datetime

scope="playlist-modify-public playlist-modify-private"

credentials = "spotify_keys.json"
with open(credentials, "r") as keys:
    api_tokens = json.load(keys)


client_id = api_tokens["client_id"]
client_secret = api_tokens["client_secret"]
redirectURI = api_tokens["redirect_uri"]
weather_api_key = api_tokens["weather_api_key"]
username = api_tokens["username"]

weather_music = {
    'thunderstorm': ['rock', 'metal'],
    'rain': ['jazz', 'lofi'],
    'snow': ['classical', 'ambient'],
    'clear': ['pop', 'dance'],
    'clouds': ['indie', 'alternative'],
    'mist': ['ambient', 'downtempo'],
    'drizzle': ['jazz', 'lofi'],
    'fog': ['ambient', 'classical']
}


token = util.prompt_for_user_token(username, scope, client_id=client_id,
                           client_secret=client_secret,
                           redirect_uri=redirectURI)
sp = spotipy.Spotify(auth=token)


def get_playlist(city): 
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    weather_condition = weather_data['weather'][0]['main'].lower()
    temperature = weather_data['main']['temp']

    if weather_condition in weather_music:
        genres = weather_music[weather_condition]
    
    else:
        genres = ['pop']  
    tracks = []
    for genre in genres:
        results = sp.search(
            q='genre:'+genre,
            type='track'
        )
        tracks.extend([track['uri'] for track in results['tracks']['items']])

    tracks = list(set(tracks))[:20]
   
    playlist_info = f"Weather-based playlist for {city}. Weather: {weather_condition}. Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}" 
    my_playlist = sp.user_playlist_create(user=username, name=city, public=True, description=playlist_info)
    sp.user_playlist_add_tracks(username, my_playlist['id'], tracks)

    return my_playlist['id']