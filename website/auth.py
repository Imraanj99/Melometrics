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
    identity = []
    iter = 0
    while True:
        offset = iter * 50
        iter += 1
        curGroup = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
        for idx, item in enumerate(curGroup):
            tracks = item['track']
            val = [tracks['id']]
            iden = [tracks['name']]
            iden.append(tracks['artists'][0]['name'])

            identity += [iden]
            results += val
        if (len(curGroup) < 50):
            break
        if (len(results)>100):
            break
    features = []
    for i in range(0,len(results),50):
        feature=sp.audio_features(results[i:i+50])
        features += feature
    df2 = pd.DataFrame(features) 
    df1 = pd.DataFrame(identity, columns=["Song","Artists"])
    df0 = df1.join(df2)
    df3 = df0.reset_index().rename(columns={'index': '#'})
    df3.index = df3.index + 1
    df = df3.drop(['key','loudness','mode','liveness','type','id','uri','track_href','analysis_url','time_signature'],axis=1)
    #df.to_csv('songs.csv', index=False)
    header = "Liked songs"
    flash('Tracks retrieved successfully', category='success')
    return render_template('table.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header)
    #return redirect(url_for('auth.home', _external=True))

@auth.route('top_tracks')
def top_tracks():
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
        top_tracks = sp.current_user_top_tracks(limit=50, offset=offset)
        for item in top_tracks["items"]:
            val = [item["name"]]
            val.append(item["artists"][0]["name"])
            results += [val]
        if (len(results)>99):
            break  
    df1 = pd.DataFrame(results, columns=["Song","Artists"])
    df1.index = df1.index + 1
    df = df1.reset_index().rename(columns={'index': '#'})
    #rename later
    specific = "(medium term)"
    header = "Top Tracks " + specific
    flash('Successfully retrieved your top 100 Tracks'+header, category='Success')
    return render_template('table2.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header)

@auth.route('top_tracks_short')
def top_tracks_short():
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
        top_tracks = sp.current_user_top_tracks(limit=50, offset=offset,time_range='short_term')
        for item in top_tracks["items"]:
            val = [item["name"]]
            val.append(item["artists"][0]["name"])
            results += [val]
        if (len(results)>99):
            break  
    df1 = pd.DataFrame(results, columns=["Song","Artists"])
    df1.index = df1.index + 1
    df = df1.reset_index().rename(columns={'index': '#'})
    #rename later
    specific = "(Recent)"
    header = "Top Tracks " + specific
    flash('Successfully retrieved your top 100 Tracks'+header, category='Success')
    return render_template('table2.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header)

@auth.route('top_tracks_long')
def top_tracks_long():
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
        top_tracks = sp.current_user_top_tracks(limit=50, offset=offset,time_range='long_term')
        for item in top_tracks["items"]:
            val = [item["name"]]
            val.append(item["artists"][0]["name"])
            results += [val]
        if (len(results)>99):
            break  
    df1 = pd.DataFrame(results, columns=["Song","Artists"])
    df1.index = df1.index + 1
    df = df1.reset_index().rename(columns={'index': '#'})
    #rename later
    specific = "(Long term)"
    header = "Top Tracks " + specific
    flash('Successfully retrieved your top 100 Tracks'+header, category='Success')
    return render_template('table2.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header)



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
            # will have to be changed. try find out why url for is not working here
            #redirect_uri='http://18.171.181.89/redir',
            redirect_uri='http://127.0.0.1:5001/redir',
            #redirect_uri=url_for('auth.redir', _external=True),
            scope="user-library-read playlist-read-private user-top-read") 