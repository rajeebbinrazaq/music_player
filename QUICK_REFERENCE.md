# 🎵 Music Player - Quick Reference Card

## 🚀 Quick Start (3 Steps)

### 1. Get YouTube API Key
```
Visit: https://console.cloud.google.com/
Enable: YouTube Data API v3
Create: API Key
```

### 2. Configure API Key
```bash
cd /opt/bench/bench-expiriments/apps/music_player
./setup.sh
```
Or manually:
```bash
bench --site experiments.bench set-config youtube_api_key "YOUR_KEY"
```

### 3. Access Music Player
```
http://localhost:8002/music-player
```

---

## 📍 Important URLs

| What | URL |
|------|-----|
| **Music Player** | http://localhost:8002/music-player |
| **Manage Playlists** | http://localhost:8002/app/music-playlist |
| **Manage Songs** | http://localhost:8002/app/youtube-song |
| **ERPNext Desk** | http://localhost:8002/app |

---

## 🎮 Player Controls

| Action | How |
|--------|-----|
| **Play/Pause** | Click ▶/⏸ button |
| **Next Song** | Click ⏭ button |
| **Previous Song** | Click ⏮ button |
| **Seek** | Click on progress bar |
| **Volume** | Click on volume bar |
| **Mute/Unmute** | Click 🔊 button |

---

## ➕ Adding Music

### Method 1: Search
```
1. Type search query (e.g., "lofi music")
2. Click "Search"
3. Click any song to play
```

### Method 2: URL
```
1. Copy YouTube URL
2. Paste in search bar
3. Click "Add URL"
```

### Method 3: Demo Data
```bash
bench --site experiments.bench console
```
```python
from music_player.music_player.demo_data import create_demo_data
create_demo_data()
```

---

## 📚 Creating Playlists

```
1. Go to: http://localhost:8002/app/music-playlist
2. Click "New"
3. Enter name and description
4. Add songs from table
5. Save
6. Click "Play Playlist"
```

---

## 🔧 Useful Commands

### Start Bench
```bash
cd /opt/bench/bench-expiriments
bench start
```

### Migrate Database
```bash
bench --site all migrate
```

### Build Assets
```bash
bench build --app music_player
```

### Check API Key
```bash
bench --site experiments.bench console
```
```python
import frappe
print(frappe.conf.get('youtube_api_key'))
```

### View Logs
```bash
bench --site experiments.bench console
```
```python
frappe.get_doc('Error Log', {'error': ['like', '%youtube%']})
```

---

## 📊 API Quota

| Item | Cost | Daily Limit |
|------|------|-------------|
| **Search** | 100 units | ~100 searches |
| **Video Details** | 1 unit | ~10,000 requests |
| **Total Quota** | - | 10,000 units |

**Monitor at**: https://console.cloud.google.com/apis/dashboard

---

## 🎨 Features

✅ YouTube search integration  
✅ Add songs from URLs  
✅ Create playlists  
✅ Beautiful modern UI  
✅ Full playback controls  
✅ Progress tracking  
✅ Volume control  
✅ Responsive design  
✅ Smooth animations  

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| **API key error** | Run `./setup.sh` or set manually |
| **Songs not playing** | Check browser console, verify video availability |
| **Search not working** | Verify API key, check quota |
| **Page not loading** | Ensure `bench start` is running |
| **Quota exceeded** | Wait for reset (midnight PT) or request increase |

---

## 📖 Documentation

| File | Purpose |
|------|---------|
| **README.md** | Complete usage guide |
| **YOUTUBE_API_SETUP.md** | API setup instructions |
| **PROJECT_SUMMARY.md** | Project overview |
| **setup.sh** | Interactive setup |

---

## 🔗 External Resources

- [YouTube API Docs](https://developers.google.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Frappe Docs](https://frappeframework.com/docs)
- [YouTube IFrame API](https://developers.google.com/youtube/iframe_api_reference)

---

## 💡 Pro Tips

1. **Cache searches** to save API quota
2. **Use demo data** for testing
3. **Monitor quota** in Google Cloud Console
4. **Restrict API key** for security
5. **Create playlists** to organize music
6. **Use keyboard shortcuts** (space = play/pause)

---

## 🎯 File Locations

```
/opt/bench/bench-expiriments/apps/music_player/
├── music_player/music_player/
│   ├── doctype/              # DocTypes
│   ├── www/music-player/     # Web interface
│   ├── youtube_api.py        # API integration
│   └── demo_data.py          # Sample data
├── README.md                 # Main docs
├── YOUTUBE_API_SETUP.md      # API guide
├── PROJECT_SUMMARY.md        # Overview
└── setup.sh                  # Setup script
```

---

## 🎊 Quick Win

**Get started in 2 minutes:**

```bash
# 1. Configure API key
cd /opt/bench/bench-expiriments/apps/music_player
./setup.sh

# 2. Open browser
# Visit: http://localhost:8002/music-player

# 3. Search for music
# Type "lofi music" and click Search

# 4. Enjoy! 🎧
```

---

**Need help?** Check README.md or YOUTUBE_API_SETUP.md

**Happy listening! 🎵✨**
