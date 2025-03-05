import React, { useState } from "react";

function App() {
  const [mood, setMood] = useState("");
  const [platform, setPlatform] = useState("spotify");
  const [playlist, setPlaylist] = useState(null);
  const [error, setError] = useState("");

  const generatePlaylist = async () => {
    setError("");
    setPlaylist(null);

    if (!mood) {
      setError("Please enter a mood.");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/generate_playlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mood, platform }),
      });

      const data = await response.json();
      if (response.ok) {
        setPlaylist(data);
      } else {
        setError(data.error || "Something went wrong.");
      }
    } catch (err) {
      setError("Failed to connect to the backend.");
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "50px" }}>
      <h1>MoodSpin - AI Playlist Generator</h1>
      <input
        type="text"
        placeholder="Enter a mood (e.g., chill, gym, road trip)"
        value={mood}
        onChange={(e) => setMood(e.target.value)}
        style={{ padding: "10px", width: "300px", marginBottom: "10px" }}
      />
      <br />
      <select value={platform} onChange={(e) => setPlatform(e.target.value)}>
        <option value="spotify">Spotify</option>
        <option value="youtube">YouTube</option>
      </select>
      <br />
      <button onClick={generatePlaylist} style={{ marginTop: "10px", padding: "10px 20px" }}>
        Generate Playlist
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {playlist && (
        <div style={{ marginTop: "20px" }}>
          {playlist.playlist_url ? (
            <a href={playlist.playlist_url} target="_blank" rel="noopener noreferrer">
              Open Spotify Playlist
            </a>
          ) : (
            <ul>
              {playlist.tracks.map((track, index) => (
                <li key={index}>
                  <a href={track.url} target="_blank" rel="noopener noreferrer">
                    {track.title || track.name} - {track.artist || ""}
                  </a>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
