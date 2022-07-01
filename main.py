from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CHART_NAME = 'hot-100' 

############# GET SONGS ################
date = ''
year = date.split('-')[0]
while len(date.split('-')) != 3 and len(date) != 10:
    date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

PLAYLIST_NAME = f'{date} Billboard 100'

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")

website = response.text
soup = BeautifulSoup(website, 'html.parser')
titles = soup.select('li ul li h3#title-of-a-story')

song_titles = [title.getText().strip() for title in titles]

############ SPOTIFY AUTH #############
OAUTH_AUTHORIZE_URL= 'https://accounts.spotify.com/authorize'
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/",
        client_id="MYCLIENTID",
        client_secret="MYCLIENTSECRET",
        show_dialog=True,
        cache_path="token.txt"
    )
)

###### check if playlist already exists     ########
user_id = sp.current_user()['id']
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


########### ADD SONGS ##########
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
