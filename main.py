from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

## GET SONGS ###
date = ''
#date = '2022-04-12'  ## Test
year = date.split('-')[0]
while len(date.split('-')) != 3 and len(date) != 10:
    date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

CHART_NAME = 'hot-100'
CHART_NAME = 'germany-songs-hotw'
PLAYLIST_NAME = f'{date} Billboard 100'
PLAYLIST_NAME = f'{date} Billboard GERMANY'

#response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
response = requests.get(f"https://www.billboard.com/charts/{CHART_NAME}/{date}/")

website = response.text
soup = BeautifulSoup(website, 'html.parser')
titles = soup.select('li ul li h3#title-of-a-story')

song_titles = [title.getText().strip() for title in titles]

## SPOTIFY AUTH ##
OAUTH_AUTHORIZE_URL= 'https://accounts.spotify.com/authorize'
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/",
        client_id="f7d8d10fed0e41b38c91097e2721e9aa",
        client_secret="49a0b1a9a0eb414db59b4bdded83ed89",
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()['id']

# check if playlist already exists
playlists = sp.user_playlists(user=user_id)['items']
playlist_name_found = False
for playlist in playlists:
    if playlist['name'] == PLAYLIST_NAME:
        playlist_name_found = True
        playlist_id = playlist['id']


if not playlist_name_found:
    playlist = sp.user_playlist_create(user=user_id, name=PLAYLIST_NAME, public=False, collaborative=False)
    playlist_id = playlist['id']
else:
    print("The playlist already exists.")
    quit()

uri_list = []

for track in song_titles:
    query = f'track:{track} year:{year}'
    artist = sp.search(q=query, limit = 1, type='track')
    try:
        uri = artist['tracks']['items'][0]['uri']
        uri_list.append(uri)
    except(IndexError):
        continue

sp.playlist_add_items(playlist_id=playlist_id, items=uri_list)