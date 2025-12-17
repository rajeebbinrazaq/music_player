import frappe

def get_context(context):
	context.no_cache = 1
	
	# Get playlist if specified
	playlist_name = frappe.form_dict.get('playlist')
	if playlist_name:
		context.playlist = frappe.get_doc('Music Playlist', playlist_name)
	else:
		context.playlist = None
	
	# Get all playlists for sidebar
	context.playlists = frappe.get_all('Music Playlist', 
		fields=['name', 'playlist_name', 'cover_image'],
		order_by='modified desc'
	)
	
	# Get favorites if specified
	show_favorites = frappe.form_dict.get('favorites')
	filters = {}
	if show_favorites:
		filters['is_favorite'] = 1

	# Get all songs
	if context.playlist and context.playlist.songs:
		song_names = [s.song for s in context.playlist.songs]
		filters['name'] = ['in', song_names]
	
	context.all_songs = frappe.get_all('YouTube Song',
		filters=filters,
		fields=['name', 'title', 'youtube_id', 'thumbnail', 'channel', 'duration', 'is_favorite'],
		order_by='modified desc',
		limit=50
	)
	
	# Disable standard header and footer to keep custom app look
	context.no_header = 1
	context.no_footer = 1
