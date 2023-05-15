# CreatePlaylistsSpotifyAPI

# This is a Flask application, that demonstrates how to create a web app with blueprints in Flask, that handles authorization to the Spotify API, creating playlist on the behalf of the user and adding songs to the created playlist using  HTTP requests with the requests library.

# you can find the follow along atricle for building this project here: https://medium.com/@austejamitz/exploring-the-spotify-api-creating-playlists-using-flask-and-requests-library-604da7623361

# Installation
Clone the repository to your local machine using git bash:
git clone https://github.com/austechuu/CreatePlaylistsSpotifyAPI.git


# Change into the project directory:
cd CreatePlaylistsSpotifyAPI


# Install the required dependencies using pip:
pip install -r requirements.txt


# Usage
Set up your Spotify Developer account and create a new app to obtain the necessary credentials (client ID and client secret).

# Create the configuration file (config.py) with your Spotify credentials and prefefined constants:
# config.py
CLIENT_ID = '<your_client_id>'
CLIENT_SECRET = '<your_client_secret>'
REDIRECT_URI = 'http://localhost:5000/callback'
SCOPE = "playlist-read-private, playlist-read-collaborative, playlist-modify-private, playlist-modify-public"
TOKEN_URL = 'https://accounts.spotify.com/api/token'
AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'
USER_PROFILE_URL = SPOTIFY_API_BASE_URL + '/me'



# Run the Flask app using the following command:
cd your/flask/path/create_playlists
set FLASK_APP=app.py

Access the app in your web browser at http://localhost:5000.

# Project Structure
The project follows the following directory structure:

create_playlists/app.py: contains the main instance of the Flask app
create_playlists/__init__.py: contains the factory function
create_playlists/auth.py: contains the auth_bp blueprint and it's routes, which are responsible for the authorization flow
create_playlists/playlists.py: contains the playlists_bp blueprint and it's routes, which are responsible for creating and adding songs to a playlist.
