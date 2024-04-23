from flask import session, url_for
import spotipy
from spotipy import SpotifyOAuth
import time
import numpy as np
from secret_info import ClientID, ClientSecret
import os

# This function connects to the API, defines the requested scope and outlines the redirect address once the user has logged in

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id= ClientID,
            client_secret= ClientSecret,
            #redirect_uri='http://18.171.150.137/redir',
            #redirect_uri='http://127.0.0.1:5000/redir',
            redirect_uri=url_for('auth.redir', _external=True),
            scope="user-library-read playlist-read-private user-top-read playlist-modify-public playlist-modify-private user-read-private user-read-email") 

# This function retrives the session token
# It is able to check for an existing token, renew and expired token, or generate a new token

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

# This token aims to verify if there is a token, and if it is still valid
# This is used to ensure that only logged in members are able to access parts of the website where user data is manipulated or displayed
# This redirects to the log in page if someone attempt to access something without the correct authorisation

def check_authorised():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return False
    return True

# this function return user information

def get_user():
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    return sp.current_user()
    
    
def get_image_path(value):
    # Ensure the value is within the acceptable range
    if not 0 <= value <= 1:
        #raise ValueError("Value must be between 0 and 1.")
        return "value Error"
    
    # define an array of which increments by 0.1 from 0-1 and then run each datapoint through it, assiging a specific f string corresponding to an image of 1-10 filled in dots to visually represent the datapoints between 0 and 1

    thresholds = [x for x in np.arange(0,1,0.1)]

    for upper_bound in thresholds:
        if value <= upper_bound:
            break

    image_path = f"/static/images/{'img_'+str(int((upper_bound)*10))}.png"

    # return image while AND value, as value remains important for sorting reasons.

    return f'<img src="{image_path}" width="120" data-value="{value}" />'

def clean_cache():
    cache_file = '.cache'
    print('clearing cache')
    if os.path.exists(cache_file):
        os.remove(cache_file)
    