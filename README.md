# Music Player App for ERPNext

Developed by **[nightcoderrbr](https://github.com/nightcoderrbr)** | [View Source](https://github.com/nightcoderrbr/music_player)

A beautiful, modern music player application for ERPNext that integrates with YouTube's free API to search, play, and manage your favorite music.

## Features

✨ **Modern UI Design**
- Beautiful gradient-based design with dark theme
- Smooth animations and transitions
- Responsive layout
- Premium glassmorphism effects

🎵 **Music Management**
- Search YouTube for music
- Add songs directly from YouTube URLs
- Create and manage playlists
- Store song metadata (title, channel, thumbnail, duration)

🎧 **Player Features**
- Full playback controls (play, pause, next, previous)
- Progress bar with seek functionality
- Volume control
- Real-time progress updates
- Embedded YouTube player

📚 **Library Management**
- Browse all songs
- Organize songs into playlists
- Quick access to playlists from sidebar

## Installation

### 1. Install the App

The app is already created and installed. If you need to reinstall:

```bash
cd /opt/bench/bench-expiriments
bench --site all install-app music_player
```

### 2. Configure YouTube API Key

To use YouTube integration, you need a free YouTube Data API v3 key:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **YouTube Data API v3**
4. Create credentials (API Key)
5. Copy your API key

Add the API key to your site configuration:

```bash
cd /opt/bench/bench-expiriments
bench --site experiments.bench set-config youtube_api_key "YOUR_API_KEY_HERE"
```

Replace `YOUR_API_KEY_HERE` with your actual YouTube API key.

### 3. Migrate Database

```bash
bench --site all migrate
```

### 4. Start Bench (if not already running)

```bash
bench start
```

## Usage

### Access the Music Player

1. Open your browser and navigate to:
   ```
   http://localhost:8002/music-player
   ```

2. Or from ERPNext:
   - Go to **Music Player** module
   - Click on **Music Playlist** or **YouTube Song**

### Adding Songs

**Method 1: Search YouTube**
1. Enter a search query in the search bar
2. Click "Search"
3. Click on any song from the results to play it
4. Songs are automatically added to your library

**Method 2: Add from URL**
1. Copy a YouTube video URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
2. Paste it in the search bar
3. Click "Add URL"
4. The song will be added to your library

### Creating Playlists

1. Go to **Music Playlist** doctype
2. Click "New"
3. Enter playlist name and description
4. Add songs from the "Songs" table
5. Save the playlist
6. Click "Play Playlist" button to start playing

### Playing Music

- Click on any song card to start playing
- Use the player controls at the bottom:
  - ⏮ Previous song
  - ▶/⏸ Play/Pause
  - ⏭ Next song
  - 🔊 Volume control
- Click on the progress bar to seek
- Click on the volume bar to adjust volume

## DocTypes

### YouTube Song
Stores information about individual songs:
- Title
- YouTube Video ID
- Thumbnail URL
- Duration
- Channel name
- Description

### Music Playlist
Manages collections of songs:
- Playlist Name
- Description
- Cover Image
- Songs (child table)

### Playlist Song (Child Table)
Links songs to playlists:
- Song reference
- Song title (auto-fetched)
- Duration (auto-fetched)

## API Methods

The app provides several whitelisted API methods:

### `search_youtube(query, max_results=10)`
Search YouTube for music videos.

### `get_video_details(video_id)`
Get detailed information about a specific YouTube video.

### `extract_video_id_from_url(url)`
Extract video ID from various YouTube URL formats.

### `add_song_from_url(url)`
Add a song to the library from a YouTube URL.

## File Structure

```
music_player/
├── music_player/
│   ├── doctype/
│   │   ├── music_playlist/
│   │   ├── youtube_song/
│   │   └── playlist_song/
│   ├── www/
│   │   └── music-player/
│   │       ├── index.html
│   │       └── index.py
│   └── youtube_api.py
├── hooks.py
└── modules.txt
```

## Technologies Used

- **Backend**: Python, Frappe Framework
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: YouTube Data API v3
- **Player**: YouTube IFrame API

## Troubleshooting

### "YouTube API Key not configured" Error
Make sure you've added your YouTube API key to the site configuration:
```bash
bench --site experiments.bench set-config youtube_api_key "YOUR_KEY"
```

### Songs not playing
1. Check browser console for errors
2. Ensure YouTube IFrame API is loaded
3. Check if the video is available in your region
4. Verify the video ID is correct

### Search not working
1. Verify your YouTube API key is valid
2. Check if you've exceeded the API quota (10,000 units/day for free tier)
3. Check the Error Log in ERPNext for detailed error messages

## API Quota Management

YouTube Data API v3 has a free quota of 10,000 units per day:
- Search: 100 units per request
- Video details: 1 unit per request

This allows approximately:
- 100 searches per day, or
- 10,000 video detail requests per day

## Future Enhancements

- [ ] Offline playback support
- [ ] Lyrics integration
- [ ] Audio visualization
- [ ] Social sharing features
- [ ] User preferences and history
- [ ] Advanced search filters
- [ ] Playlist collaboration
- [ ] Mobile app version

## License

MIT License

## Support

For issues and questions:
1. Check the ERPNext forum
2. Review the YouTube API documentation
3. Check browser console for errors
4. Review ERPNext Error Log

## Credits

Built with ❤️ using:
- ERPNext/Frappe Framework
- YouTube Data API v3
- YouTube IFrame Player API

---

**Note**: This app uses YouTube's free API and is subject to YouTube's Terms of Service. Make sure to comply with YouTube's API usage policies.
