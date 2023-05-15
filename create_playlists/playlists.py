# import the necessary modules
import time
from flask import Blueprint, session, redirect
import requests
import json
from create_playlists.config import USER_PROFILE_URL, SPOTIFY_API_BASE_URL

# create a blueprint to handle the playlist creation and song addition routes
playlists_bp = Blueprint('playlists', __name__, url_prefix='')


# create a playlist creation route
@playlists_bp.route('/create_playlist')
def create_playlist_route():
    create_playlist("My new playlist")
    time.sleep(5)
    return redirect('/add_songs')


# create a songs' addition route
@playlists_bp.route('/add_songs')
def add_songs_route():
    # define the id of the chosen playlist to retrieve the songs from
    target_playlist_id = '37i9dQZEVXbNG2KDcFcKOF'
    # getting the playlist id from the session
    playlist_id = session.get('playlist_id')
    if playlist_id is None:
        return 'Error: Playlist ID not found in session'

    # adding songs to the playlist and getting the added tracks and number of tracks added
    added_tracks, num_tracks = add_songs_to_playlist(target_playlist_id, playlist_id)

    if num_tracks > 0:
        # formatting a message with the number of tracks added and the track names
        track_names = ', '.join(added_tracks)
        return f"{num_tracks} tracks successfully added to the playlist with ID {playlist_id}. The added tracks are: {track_names}"
    else:
        return f"No tracks were added to the playlist with ID {playlist_id}"


# helper function _get_user_id to retrieve the user's id
def _get_user_id():
    headers = {'Authorization': f'Bearer {session["access_token"]}'}
    response = requests.get(USER_PROFILE_URL, headers=headers)
    user_profile = json.loads(response.content)
    return user_profile['id']


# function, that handles the actual creation of the playlist
def create_playlist(name, public=True):
    # get the user ID
    user_id = _get_user_id()
    # define the URL, that the POST request is going to be made to
    url = SPOTIFY_API_BASE_URL + f'/users/{user_id}/playlists'
    # define the headers and data for the request
    headers = {'Authorization': f'Bearer {session["access_token"]}', 'Content-Type': 'application/json'}
    # send the POST request
    data = {'name': name, 'public': public}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        # getting the ID of the created playlist and storing it in the session
        playlist_id = response.json()['id']
        session['playlist_id'] = playlist_id
        print(f"Playlist '{name}' successfully created with ID: {playlist_id}")
        return playlist_id
    else:
        # if the request fails, an error message will get printed and return None
        print(f"Failed to create playlist '{name}' with status code {response.status_code}")
        return None


# function, that fetches up to 10 tracks from a selected playlist
def _get_playlist_tracks(url, limit=10):
    # set up the authorization header with the access token
    headers = {'Authorization': f'Bearer {session["access_token"]}'}
    response = requests.get(url, headers=headers)

    # extract track objects from API response.
    tracks = []
    while True:
        data = response.json()
        tracks.extend(data['items'])

        if data['next'] and len(tracks) < limit:
            response = requests.get(data['next'], headers=headers)
        else:
            break

    # return the list of track objects, up to the specified limit
    return tracks[:limit]


# function, that handles the addition of the songs retrieved from target playlist into the playlist we created in /create_playlist
def add_songs_to_playlist(target_playlist_id, playlist_id, limit=10):
    # getting the tracks from a predefined playlist
    playlist_url = SPOTIFY_API_BASE_URL + f'/playlists/{target_playlist_id}/tracks'
    playlist_tracks = _get_playlist_tracks(playlist_url, limit=limit)

    # extracting the track URIs from the playlist tracks
    tracks = [{'uri': track['track']['uri']} for track in playlist_tracks]

    # defining the URL, headers, and data for the request to add tracks to the playlist
    url = SPOTIFY_API_BASE_URL + f'/playlists/{playlist_id}/tracks'
    headers = {'Authorization': f'Bearer {session["access_token"]}', 'Content-Type': 'application/json'}
    data = {'uris': [track['uri'] for track in tracks]}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        # if the response is successful, number and names of the tracks, that were added, are printed
        added_tracks = [track['track']['name'] for track in playlist_tracks[:limit]]
        num_tracks = len(added_tracks)
        print(f"{num_tracks} tracks successfully added to the playlist with ID: {playlist_id}")
        print(f"Added tracks: {', '.join(added_tracks)}")
        return added_tracks, num_tracks
    else:
        # if the response is unsuccessful, an empty list and zero are returned
        print(f"Failed to add tracks to the playlist with status code {response.status_code}")
        return [], 0
