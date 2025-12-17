# Copyright (c) 2025, Music Player and contributors
# For license information, please see license.txt

"""
Demo data script to create sample songs and playlists
Run this from bench console:
    bench --site experiments.bench console
    >>> from music_player.music_player.demo_data import create_demo_data
    >>> create_demo_data()
"""

import frappe


def create_demo_data():
	"""
	Create demo songs and playlists
	Note: This requires a valid YouTube API key to be configured
	"""
	
	# Sample YouTube video IDs (popular royalty-free music)
	demo_videos = [
		{
			'youtube_id': 'jfKfPfyJRdk',
			'title': 'Lofi Hip Hop Music',
			'channel': 'Lofi Girl',
			'thumbnail': 'https://i.ytimg.com/vi/jfKfPfyJRdk/hqdefault.jpg',
			'duration': 'PT2H0M0S',
			'description': 'Lofi hip hop music - beats to relax/study to'
		},
		{
			'youtube_id': '5qap5aO4i9A',
			'title': 'Relaxing Jazz Music',
			'channel': 'Cafe Music BGM channel',
			'thumbnail': 'https://i.ytimg.com/vi/5qap5aO4i9A/hqdefault.jpg',
			'duration': 'PT3H0M0S',
			'description': 'Relaxing Jazz Piano Music'
		},
	]
	
	print("Creating demo songs...")
	created_songs = []
	
	from music_player.music_player.youtube_api import add_song_from_url
	
	for video in demo_videos:
		try:
			# Use add_song_from_url which handles duplicates and oEmbed fallback
			url = f"https://www.youtube.com/watch?v={video['youtube_id']}"
			print(f"Adding {video['title']}...")
			song = add_song_from_url(url)
			created_songs.append(song)
			print(f"✅ processed: {song.title}")
		except Exception as e:
			print(f"❌ Error processing {video['title']}: {str(e)}")
	
	# Create a demo playlist
	print("\nCreating demo playlist...")
	
	playlist_name = "Chill Vibes"
	
	if not frappe.db.exists('Music Playlist', playlist_name):
		try:
			playlist = frappe.get_doc({
				'doctype': 'Music Playlist',
				'playlist_name': playlist_name,
				'description': 'A collection of relaxing music for studying and working',
				'songs': [
					{
						'song': song.name,
						'song_title': song.title,
						'duration': song.duration
					} for song in created_songs
				]
			})
			playlist.insert()
			print(f"✅ Created playlist: {playlist.playlist_name}")
		except Exception as e:
			print(f"❌ Error creating playlist: {str(e)}")
	else:
		print(f"⏭️  Playlist already exists: {playlist_name}")
	
	frappe.db.commit()
	
	print("\n" + "="*50)
	print("Demo data creation complete!")
	print("="*50)
	print(f"\n📊 Summary:")
	print(f"   Songs created: {len(created_songs)}")
	print(f"   Playlists created: 1")
	print(f"\n🎵 Access the music player at:")
	print(f"   http://localhost:8002/music-player")
	print("\n")


def create_sample_songs_from_api(search_query="lofi music", max_results=5):
	"""
	Create sample songs by searching YouTube
	Requires YouTube API key to be configured
	"""
	from music_player.music_player.youtube_api import search_youtube, add_song_from_url
	
	try:
		print(f"Searching YouTube for: {search_query}")
		results = search_youtube(search_query, max_results)
		
		print(f"\nFound {len(results)} results. Adding to library...")
		
		for result in results:
			try:
				# Create song from video ID
				if not frappe.db.exists('YouTube Song', {'youtube_id': result['video_id']}):
					song = frappe.get_doc({
						'doctype': 'YouTube Song',
						'title': result['title'],
						'youtube_id': result['video_id'],
						'thumbnail': result['thumbnail'],
						'channel': result['channel'],
						'description': result['description'],
						'duration': 'PT0M0S'  # Duration not available from search
					})
					song.insert()
					print(f"✅ Added: {song.title}")
				else:
					print(f"⏭️  Already exists: {result['title']}")
			except Exception as e:
				print(f"❌ Error adding {result['title']}: {str(e)}")
		
		frappe.db.commit()
		print("\n✅ Sample songs added successfully!")
		
	except Exception as e:
		print(f"❌ Error: {str(e)}")
		print("\nMake sure you have configured your YouTube API key:")
		print("bench --site experiments.bench set-config youtube_api_key \"YOUR_KEY\"")


if __name__ == '__main__':
	create_demo_data()
