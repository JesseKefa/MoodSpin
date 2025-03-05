from flask import Flask, request, jsonify
from spotify_api import search_songs as search_spotify_songs, create_playlist
from youtube_api import search_youtube_songs
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route("/generate_playlist", methods=["POST"])
def generate_playlist():
    """Generates a playlist based on mood."""
    data = request.json
    mood = data.get("mood")
    platform = data.get("platform", "spotify")
    
    if not mood:
        return jsonify({"error": "Mood is required."}), 400
    
    if platform == "spotify":
        user_id = os.getenv("SPOTIFY_USER_ID")  # Set your user ID in .env
        songs = search_spotify_songs(mood)
        track_ids = [song['id'] for song in songs]
        playlist_url = create_playlist(user_id, f"{mood.capitalize()} Vibes", track_ids)
        return jsonify({"playlist_url": playlist_url, "tracks": songs})
    
    elif platform == "youtube":
        songs = search_youtube_songs(mood)
        return jsonify({"tracks": songs})
    
    else:
        return jsonify({"error": "Invalid platform."}), 400

if __name__ == "__main__":
    app.run(debug=True)
