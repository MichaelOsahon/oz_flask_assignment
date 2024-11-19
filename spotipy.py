import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import json
import requests
from datetime import datetime

scope="playlist-modify-public playlist-modify-private"

credentials = "spotify_keys.json"
with open(credentials, "r") as keys:
    api_tokens = json.load(keys)


client_id = api_tokens["client_id"]
client_secret = api_tokens["client_secret"]
redirectURI = api_tokens["redirect_uri"]
weather_api_key = api_tokens["weather_api_key"]
playlist_id = api_tokens["playlist_id"]
username = api_tokens["username"]



city = "London"  

weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
weather_response = requests.get(weather_url)
weather_data = weather_response.json()

weather_condition = weather_data['weather'][0]['main'].lower()
temperature = weather_data['main']['temp']

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

if weather_condition in weather_music:
    genres = weather_music[weather_condition]
else:
    genres = ['pop']  

 token = util.prompt_for_user_token(username, scope, client_id=client_id,
                           client_secret=client_secret,
                           redirect_uri=redirectURI)
sp = spotipy.Spotify(auth=token)

tracks = []
for genre in genres:
    results = sp.recommendations(
        seed_genres=[genre],
        limit=10
    )
    tracks.extend([track['uri'] for track in results['tracks']])

tracks = list(set(tracks))[:20]

sp.playlist_replace_items(playlist_id, tracks)

playlist_info = f"Weather-based playlist for {city}. Weather: {weather_condition}. Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
sp.playlist_change_details(playlist_id, description=playlist_info)


playlist_tracks = sp.playlist_tracks(playlist_id)
print("\nAdded Tracks:")
for idx, item in enumerate(playlist_tracks['items'], 1):
    track = item['track']
    print(f"{idx}. {track['name']} - {track['artists'][0]['name']}")