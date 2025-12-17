# Copyright (c) 2025, Music Player and contributors
# For license information, please see license.txt

import frappe
import requests
from urllib.parse import urlparse, parse_qs


@frappe.whitelist(allow_guest=True)
def search_youtube(query, max_results=10):
	"""
	Search YouTube videos using YouTube Data API v3
	Note: You need to set up YouTube API key in Site Config
	"""
	api_key = frappe.conf.get('youtube_api_key')
	
	if not api_key:
		frappe.throw("YouTube API Key not configured. Please add 'youtube_api_key' in site_config.json")
	
	url = "https://www.googleapis.com/youtube/v3/search"
	params = {
		'part': 'snippet',
		'q': query,
		'type': 'video',
		'maxResults': max_results,
		'key': api_key,
		'videoCategoryId': '10'  # Music category
	}
	
	try:
		response = requests.get(url, params=params)
		response.raise_for_status()
		data = response.json()
		
		results = []
		for item in data.get('items', []):
			video_id = item['id']['videoId']
			snippet = item['snippet']
			
			results.append({
				'video_id': video_id,
				'title': snippet['title'],
				'thumbnail': snippet['thumbnails']['high']['url'],
				'channel': snippet['channelTitle'],
				'description': snippet['description']
			})
			
		# Fetch content details (duration) if we have results
		if results and api_key:
			try:
				video_ids = [r['video_id'] for r in results]
				details_url = "https://www.googleapis.com/youtube/v3/videos"
				details_params = {
					'part': 'contentDetails',
					'id': ','.join(video_ids),
					'key': api_key
				}
				details_response = requests.get(details_url, params=details_params)
				if details_response.ok:
					details_data = details_response.json()
					duration_map = {}
					for item in details_data.get('items', []):
						duration_map[item['id']] = parse_duration(item['contentDetails']['duration'])
					
					# Merge duration back to results
					for result in results:
						result['duration'] = duration_map.get(result['video_id'], '')
			except Exception:
				pass # Ignore errors in second fetch, just show without duration
		
		return results
	except requests.exceptions.HTTPError as e:
		error_msg = f"YouTube API Error: {str(e)}"
		if e.response.status_code == 400:
			error_msg = "Invalid YouTube API Key or Request. Please check your API Key configuration."
			# Check for specific error reasons if available in response
			try:
				error_data = e.response.json()
				if 'error' in error_data:
					error_msg += f" Details: {error_data['error']['message']}"
			except:
				pass

		frappe.log_error("YouTube API Search Error", error_msg)
		frappe.throw(error_msg)
	except Exception as e:
		frappe.log_error("YouTube API Search Error", str(e))
		frappe.throw(f"Error searching YouTube: {str(e)}")


@frappe.whitelist(allow_guest=True)
def get_video_details(video_id):
	"""
	Get detailed information about a YouTube video
	"""
	api_key = frappe.conf.get('youtube_api_key')
	
	if not api_key:
		frappe.throw("YouTube API Key not configured")
	
	url = "https://www.googleapis.com/youtube/v3/videos"
	params = {
		'part': 'snippet,contentDetails',
		'id': video_id,
		'key': api_key
	}
	
	try:
		response = requests.get(url, params=params)
		response.raise_for_status()
		data = response.json()
		
		if not data.get('items'):
			frappe.throw("Video not found")
		
		item = data['items'][0]
		snippet = item['snippet']
		content_details = item['contentDetails']
		
		return {
			'video_id': video_id,
			'title': snippet['title'],
			'thumbnail': snippet['thumbnails']['high']['url'],
			'channel': snippet['channelTitle'],
			'description': snippet['description'],
			'duration': content_details['duration']
		}
	except requests.exceptions.HTTPError as e:
		error_msg = f"YouTube API Error: {str(e)}"
		if e.response.status_code == 400:
			error_msg = "Invalid YouTube API Key or Request. Please check your API Key configuration."
			try:
				error_data = e.response.json()
				if 'error' in error_data:
					error_msg += f" Details: {error_data['error']['message']}"
			except:
				pass
		
		frappe.log_error("YouTube API Details Error", error_msg)
		frappe.throw(error_msg)
	except Exception as e:
		frappe.log_error("YouTube API Details Error", str(e))
		frappe.throw(f"Error getting video details: {str(e)}")


@frappe.whitelist()
def extract_video_id_from_url(url):
	"""
	Extract YouTube video ID from various YouTube URL formats
	"""
	parsed_url = urlparse(url)
	
	if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
		if parsed_url.path == '/watch':
			return parse_qs(parsed_url.query).get('v', [None])[0]
		elif parsed_url.path.startswith('/embed/'):
			return parsed_url.path.split('/')[2]
	elif parsed_url.hostname == 'youtu.be':
		return parsed_url.path[1:]
	
	return None


def get_video_details_oembed(video_id):
	"""
	Get video details using oEmbed (No API Key required)
	"""
	try:
		oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
		response = requests.get(oembed_url)
		response.raise_for_status()
		data = response.json()
		
		# oEmbed doesn't provide duration or description, so we use placeholders
		return {
			'video_id': video_id,
			'title': data.get('title', 'Unknown Title'),
			'thumbnail': data.get('thumbnail_url', ''),
			'channel': data.get('author_name', 'Unknown Artist'),
			'description': 'Added via oEmbed',
			'duration': 'PT0M0S' # Unknown duration
		}
	except Exception as e:
		frappe.log_error(f"oEmbed Error: {str(e)}")
		return None


def get_or_create_song(video_id):
	"""
	Get existing song doc or create new one from YouTube details
	"""
	existing = frappe.db.get_value('YouTube Song', {'youtube_id': video_id})
	if existing:
		return frappe.get_doc('YouTube Song', existing)
	
	# Fetch details and create
	details = None
	
	# 1. Try API first if configured
	if frappe.conf.get('youtube_api_key'):
		try:
			details = get_video_details(video_id)
		except Exception:
			pass
	
	# 2. Try oEmbed if API failed or not configured
	if not details:
		details = get_video_details_oembed(video_id)
		
	if not details:
		frappe.throw("Could not fetch video details from YouTube.")
		
	song = frappe.get_doc({
		'doctype': 'YouTube Song',
		'title': details['title'],
		'youtube_id': video_id,
		'thumbnail': details['thumbnail'],
		'channel': details['channel'],
		'description': details['description'],
		'duration': details['duration']
	})
	song.insert(ignore_permissions=True)
	return song


@frappe.whitelist(allow_guest=True)
def add_song_from_url(url):
	"""
	Add a song to the library from a YouTube URL
	"""
	video_id = extract_video_id_from_url(url)
	
	if not video_id:
		frappe.throw("Invalid YouTube URL")
	
	return get_or_create_song(video_id)


def parse_duration(duration_str):
	"""
	Parse ISO 8601 duration format (e.g., PT4M13S) to human readable format
	"""
	import re
	
	match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
	if not match:
		return duration_str
	
	hours, minutes, seconds = match.groups()
	
	hours, minutes, seconds = match.groups()
	
	h = int(hours) if hours else 0
	m = int(minutes) if minutes else 0
	s = int(seconds) if seconds else 0
	
	if h > 0:
		return f"{h}:{m:02d}:{s:02d}"
	else:
		return f"{m}:{s:02d}"


@frappe.whitelist(allow_guest=True)
def toggle_favorite(video_id):
	"""
	Toggle favorite status of a song. 
	If song doesn't exist, it creates it first.
	"""
	# Get or create the song
	song = get_or_create_song(video_id)
	
	# Toggle favorite
	song.is_favorite = 0 if song.is_favorite else 1
	song.save(ignore_permissions=True)
	
	return song.is_favorite


@frappe.whitelist(allow_guest=True)
def get_playlists():
	return frappe.get_all('Music Playlist', fields=['name', 'playlist_name'], order_by='modified desc')


@frappe.whitelist(allow_guest=True)
def create_playlist(playlist_name):
	if frappe.db.exists('Music Playlist', {'playlist_name': playlist_name}):
		frappe.throw('Playlist already exists')
	
	playlist = frappe.get_doc({
		'doctype': 'Music Playlist',
		'playlist_name': playlist_name
	})
	playlist.insert(ignore_permissions=True)
	return playlist.name


@frappe.whitelist(allow_guest=True)
def add_to_playlist(playlist_name, video_id):
	playlist = frappe.get_doc('Music Playlist', playlist_name)
	
	# Get or create the song
	song_doc = get_or_create_song(video_id)
	song_name = song_doc.name

	# Check if already in playlist
	for s in playlist.songs:
		if s.song == song_name:
			frappe.msgprint("Song already in playlist")
			return
			
	playlist.append('songs', {
		'song': song_name
	})
	playlist.save(ignore_permissions=True)
	playlist.save(ignore_permissions=True)
	return True


@frappe.whitelist(allow_guest=True)
def remove_from_playlist(playlist_name, video_id):
	"""
	Remove a song from a playlist
	"""
	playlist = frappe.get_doc('Music Playlist', playlist_name)
	
	# Find song doc name from video_id
	song_name = frappe.db.get_value('YouTube Song', {'youtube_id': video_id})
	
	if not song_name:
		return
		
	# Filter out the song
	original_len = len(playlist.songs)
	playlist.songs = [s for s in playlist.songs if s.song != song_name]
	
	if len(playlist.songs) < original_len:
		playlist.save(ignore_permissions=True)
		return True
	return False





@frappe.whitelist(allow_guest=True)
def delete_song(song_name):
	"""
	Delete a song from the library
	"""
	if not frappe.db.exists('YouTube Song', song_name):
		return False

	# 1. Remove from all playlists first to avoid Link integrity error
	# Find all playlists containing this song
	references = frappe.get_all('Playlist Song', filters={'song': song_name}, fields=['parent'])
	
	unique_playlists = set([d.parent for d in references])
	
	for playlist_name in unique_playlists:
		try:
			pl = frappe.get_doc('Music Playlist', playlist_name)
			# Filter out the song
			original_len = len(pl.songs)
			pl.songs = [s for s in pl.songs if s.song != song_name]
			
			if len(pl.songs) < original_len:
				pl.save(ignore_permissions=True)
		except Exception:
			# If a playlist is corrupt or missing, just continue? 
			# Or log it. Safe to ignore for now to ensure song deletion proceeds if possible
			continue

	# 2. Delete the song
	frappe.delete_doc('YouTube Song', song_name, ignore_permissions=True)
	return True

@frappe.whitelist(allow_guest=True)
def get_library_songs(playlist=None, favorites=False):
	filters = {}
	if favorites:
		filters['is_favorite'] = 1
	
	if playlist:
		playlist_doc = frappe.get_doc('Music Playlist', playlist)
		if playlist_doc.songs:
			song_names = [s.song for s in playlist_doc.songs]
			filters['name'] = ['in', song_names]
		else:
			return [] # Empty playlist

	songs = frappe.get_all('YouTube Song',
		filters=filters,
		fields=['name', 'title', 'youtube_id', 'thumbnail', 'channel', 'duration', 'is_favorite'],
		order_by='modified desc',
		limit=50
	)

	# Parse duration for display
	for song in songs:
		if song.duration:
			song.duration = parse_duration(song.duration)
			
	return songs
