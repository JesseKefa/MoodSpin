import os
import googleapiclient.discovery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_songs(mood, limit=10):
    """Search YouTube for songs related to a mood."""
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    
    query = f"{mood} music playlist"
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=limit
    )
    
    response = request.execute()
    
    videos = []
    for item in response.get("items", []):
        video_info = {
            "title": item["snippet"]["title"],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        }
        videos.append(video_info)
    
    return videos

if __name__ == "__main__":
    mood = "chill"
    songs = search_songs(mood)
    for song in songs:
        print(f"{song['title']} - {song['url']}")
