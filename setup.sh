#!/bin/bash

# Music Player App - Quick Setup Script

echo "========================================="
echo "Music Player App - Quick Setup"
echo "========================================="
echo ""

# Check if bench is running
if ! pgrep -f "bench start" > /dev/null; then
    echo "⚠️  Warning: Bench doesn't appear to be running."
    echo "   Please run 'bench start' in another terminal first."
    echo ""
fi

# Get API key from user
echo "To use the Music Player app, you need a YouTube Data API v3 key."
echo "See YOUTUBE_API_SETUP.md for detailed instructions."
echo ""
read -p "Enter your YouTube API key (or press Enter to skip): " api_key

if [ -n "$api_key" ]; then
    echo ""
    echo "Setting up YouTube API key..."
    cd /opt/bench/bench-expiriments
    bench --site experiments.bench set-config youtube_api_key "$api_key"
    
    if [ $? -eq 0 ]; then
        echo "✅ API key configured successfully!"
    else
        echo "❌ Failed to configure API key. Please try manually:"
        echo "   bench --site experiments.bench set-config youtube_api_key \"YOUR_KEY\""
    fi
else
    echo "⏭️  Skipping API key setup."
    echo "   You can configure it later with:"
    echo "   bench --site experiments.bench set-config youtube_api_key \"YOUR_KEY\""
fi

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "📱 Access the Music Player:"
echo "   http://localhost:8002/music-player"
echo ""
echo "📚 Manage Playlists:"
echo "   http://localhost:8002/app/music-playlist"
echo ""
echo "🎵 Manage Songs:"
echo "   http://localhost:8002/app/youtube-song"
echo ""
echo "📖 Documentation:"
echo "   - README.md - General usage guide"
echo "   - YOUTUBE_API_SETUP.md - API setup instructions"
echo ""
echo "Happy listening! 🎧"
