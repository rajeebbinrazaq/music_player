# Vyb Records
YoutubeAPI based Music Player developed on frappe platform

Developed by **[rajeebbinrazaq](https://github.com/rajeebbinrazaq)** | [View Source](https://github.com/rajeebbinrazaq/music_player)

A simple, modern minimal music player application developed on frappe platform that integrates with YouTube's free API to search, play, and manage your favorite music.

**Note:** This app is not a **production-ready app** and is only for **testing purposes**.

## Features

1. **Search YouTube**
2. **Add from URL**
3. **Playlist Management**
4. **Modern UI Design**
5. **Music Management**
6. **Player Features**
7. **Library Management**



### Configure YouTube API Key

To use YouTube integration, you need a free YouTube Data API v3 key:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **YouTube Data API v3**
4. Create credentials (API Key)
5. Copy your API key

Add the API key to your site configuration:

```bash
bench --site site-name set-config youtube_api_key "YOUR_API_KEY_HERE"
```

Replace `YOUR_API_KEY_HERE` with your actual YouTube API key.

Run bench migrate

```bash
bench --site site-name migrate
```


## Usage

### Access the Music Player

1. Open your browser and navigate to:
   ```
   https://<IP_ADDRESS>/music-player
   ```

2. Or from ERPNext:
   - Go to **Music Player** module
   - Click on **Music Playlist** or **YouTube Song**


## License

MIT License


**Note**: This app uses YouTube's free API and is subject to YouTube's Terms of Service. Make sure to comply with YouTube's API usage policies.
