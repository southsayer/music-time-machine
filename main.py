from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Hello there! I'm a music time machine, which year you want to travel to?\n"
             "Type the date in this format YYYY-MM-DD: ")

response = requests.get(url="https://www.billboard.com/charts/hot-100/"+date)
bill_wpg = response.text

soup = BeautifulSoup(bill_wpg, "html.parser")
songs_list = [songs_tags.getText() for songs_tags in
              soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")]
print(songs_list)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback/",
        client_id="71912aa34c13480386542f6abb95782d",
        client_secret="1c43567949af47889143a8b0e0fab4e1",
        show_dialog=True,
        cache_path="token.txt",
        open_browser=False
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=song_uris)