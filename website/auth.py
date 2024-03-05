from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import spotipy
from spotipy import SpotifyOAuth
import time
import pandas as pd


auth = Blueprint('auth', __name__)
TOKEN_INFO = 'token_info'

@auth.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    #return render_template(auth_url)
    #print(auth_url)
    #be warned this may not work if refreshed from log in page as auth URL may now be wrong
    return render_template('login.html', authorisation=auth_url)

@auth.route('/redir')
def redir():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    flash('You have successfully logged in', category='success')
    return redirect(url_for('auth.home', _external=True))

@auth.route('/')
def home():
    session['token_info'], authorised = get_token()
    session.modified = True
    if not authorised:
        flash('Please log in', category='failure')
        return redirect(url_for('auth.login'))
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    return render_template('home.html')

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

@auth.route('/getTracks')
def get_all_tracks():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    results = []
    iter = 0
    while True:
        offset = iter * 50
        iter += 1
        curGroup = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
        for idx, item in enumerate(curGroup):
            track = item['track']
            val = [track['name']]
            val.append(track['artists'][0]['name'])

            features=sp.audio_features([track['id']])
            if "error" in features:
                print('this has worked',features)
                time.sleep(5)
            val.append(features) 
            results += [val]
            '''
        if (len(curGroup) < 50):
            break
            '''
        break
    
    df = pd.DataFrame(results, columns=["song names","artists"]) 
    df.to_csv('songs.csv', index=False)
    flash('successfully retreived tracks', category='Success')
    return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
    #return redirect(url_for('auth.home', _external=True))


#not yet used
@auth.route('/SingleInfo')
def get_single_track_info():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    results = []
    curGroup = sp.current_user_saved_tracks(limit=1, offset=1)['items']
    for idx, item in enumerate(curGroup):
        track = item['track']
        print(track['id'])
        print(sp.audio_features(track['id']))
        '''
        results.append(sp.audio_features(tracks=[track['id']]))
        print(results)
        flash('info retreived', category='Success')
        '''
    return render_template('home.html')
    '''
    while True:
        offset = iter * 50
        iter += 1
        curGroup = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
        for idx, item in enumerate(curGroup):
            track = item['track']
            val = track['name'] + " - " + track['artists'][0]['name']
            results += [val]
        if (len(curGroup) < 50):
            break
    
    df = pd.DataFrame(results, columns=["song names"]) 
    df.to_csv('songs.csv', index=False)
    flash('successfully retreived tracks', category='Success')
    return redirect(url_for('auth.home', _external=True))
    '''



@auth.route('/logout')
def logout():
    print(session)
    for key in list(session.keys()):
        print(session, '12345')
        session.pop(key)
        print(session)
    return redirect(url_for('auth.login'))

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id="8bde0ea3e6574d2199681fca5f885845",
            client_secret="75ad5e8dc0e941fc95d397b2214b11ed",
            redirect_uri=url_for('auth.redir', _external=True),
            scope="user-library-read user-read-private ")