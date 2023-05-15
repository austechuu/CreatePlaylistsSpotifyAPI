import base64
import secrets
import requests
import json
from flask import Blueprint, redirect, request, session, url_for
from create_playlists.config import CLIENT_ID, REDIRECT_URI, SCOPE, AUTH_URL, TOKEN_URL, CLIENT_SECRET

# create a blueprint to handle authorization routes
auth_bp = Blueprint('auth', __name__, url_prefix='')


# create a login route
@auth_bp.route('/login')
def login():
    state = secrets.token_hex(16)
    # set up the parameters for the authorization request
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'state': state,
        'scope': SCOPE,
        'response_type': 'code',
    }
    auth_url = AUTH_URL + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])

    return redirect(auth_url)


# create a callback route
@auth_bp.route('/callback')
def callback():
    # Retrieve the authorization code from the response
    auth_code = request.args.get('code')

    # Step 2: Exchange the authorization code for an access token
    headers = {
        'Authorization': f'Basic {base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    tokens = json.loads(response.content)

    # Step 3: Store the access token in the session
    session['access_token'] = tokens['access_token']

    # return a success message
    return redirect(url_for('playlists.create_playlist_route'))
