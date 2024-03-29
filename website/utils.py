from flask import session, redirect
import spotipy
from spotipy import SpotifyOAuth
import time

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id="8bde0ea3e6574d2199681fca5f885845",
            client_secret="75ad5e8dc0e941fc95d397b2214b11ed",
            # will have to be changed. try find out why url for is not working here
            #redirect_uri='http://18.171.181.89/redir',
            redirect_uri='http://127.0.0.1:5001/redir',
            #redirect_uri=url_for('auth.redir', _external=True),
            scope="user-library-read playlist-read-private user-top-read playlist-modify-public playlist-modify-private") 

def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid

def check_authorised():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return False
    return True

