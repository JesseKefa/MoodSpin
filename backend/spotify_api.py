import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SCOPE = "playlist-modify-public playlist-modify-private"

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE
))

def search_songs(mood, limit=10):
    """Search for songs based on mood keywords."""
    query = f"{mood} playlist"
    results = sp.search(q=query, limit=limit, type='track')
    
    tracks = []
    for item in results['tracks']['items']:
        track_info = {
            'name': item['name'],
            'artist': item['artists'][0]['name'],
            'id': item['id'],
            'url': item['external_urls']['spotify']
        }
        tracks.append(track_info)
    
    return tracks

def create_playlist(user_id, playlist_name, track_ids):
    """Create a Spotify playlist and add tracks."""
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    sp.playlist_add_items(playlist_id=playlist['id'], items=track_ids)
    return playlist['external_urls']['spotify']

if __name__ == "__main__":
    mood = "chill"
    user_id = sp.current_user()["id"]
    songs = search_songs(mood)
    track_ids = [song['id'] for song in songs]
    playlist_url = create_playlist(user_id, f"{mood.capitalize()} Vibes", track_ids)
    print(f"Playlist Created: {playlist_url}")
