from flask import Blueprint, session, redirect, render_template, flash, url_for, request
import datetime
import spotipy
import pandas as pd


from .utils import get_token, check_authorised

methods = Blueprint('methods', __name__)

# this method returns a list the users liked songs (currently up to 150 due to restriction on number or requests to spotify api)
# once cleared by spotify to leave developer mode, this can be expanded to return the full list of liked songs

@methods.route('/getTracks')
def get_all_tracks():

    #check if session valid and user still logged in

    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    
    # define and populate seperate arrays for song IDs and song names  

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

    # define a new array for audio features and populate by feeding in song IDs in batches of 50 (max size of input permitted by API)

    features = []
    for i in range(0,len(results),50):
        feature=sp.audio_features(results[i:i+50])
        features += feature

    # Create a dataframe for the featues and song/artist info and combine
    # Create a seperate column for the indexes in the dataframe and shift this to begin at 1 instead of 0

    df2 = pd.DataFrame(features) 
    df1 = pd.DataFrame(identity, columns=["Song","Artists"])
    df0 = df1.join(df2)
    df3 = df0.reset_index().rename(columns={'index': '#'})
    df3.index = df3.index + 1

    # Trim df to remove unnecessary columns and modify column headers
    # Turn duration from milliseconds to seconds and minutes

    df = df3.drop(['key','loudness','mode','liveness','type','id','uri','track_href','analysis_url','time_signature'],axis=1)
    df = df.rename(columns={'valence': 'Positivity', 'tempo': 'BPM','duration_ms':'Length'})
    def ms_to_min_sec(milliseconds):
        seconds = int((milliseconds / 1000) % 60)
        minutes = int(milliseconds / (1000 * 60))
        return f"{minutes}:{seconds:02d}"
    df['Length'] = df['Length'].apply(ms_to_min_sec)

    # Output relevant information, convert df to html and redirect to table template

    #df.to_csv('songs.csv', index=False)
    header = "Liked songs"
    flash('Tracks retrieved successfully', category='success')
    return render_template('table.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header)
    #return redirect(url_for('auth.home', _external=True))

# This uses the get_tracks function to retrieve top tracks over a short length of time 

@methods.route('/top_tracks_short')
def top_tracks_short():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    scale = 'short_term'
    specific = "(Short term)"
    df = top_tracks(scale)
    specific = "(Recent)"
    header = "Top Tracks " + specific
    flash('Successfully retrieved your top 100 Tracks'+header, category='Success')
    return render_template('table2.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header)

# This uses the get_tracks function to retrieve top tracks over a medium length of time 

@methods.route('/top_tracks_medium')
def top_tracks_medium():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    scale = 'medium_term'
    specific = "(Medium term)"
    df = top_tracks(scale)
    specific = "(medium term)"
    header = "Top Tracks " + specific
    flash('Successfully retrieved your top 100 Tracks'+header, category='Success')
    return render_template('table2.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header)


# This uses the get_tracks function to retrieve top tracks over a long length of time 

@methods.route('/top_tracks_long')
def top_tracks_long():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    scale = 'long_term'
    specific = "(Long term)"
    df = top_tracks(scale)
    header = "Top Tracks " + specific
    flash('Successfully retrieved your top 100 Tracks'+header, category='Success')
    return render_template('table2.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header,)

@methods.route('/make_playlist')
def make_playlist():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    user_id = sp.current_user()['id']
    current_date = datetime.datetime.now()
    date_now= current_date.strftime('%d-%m-%y')
    name = 'Top Tracks'+ date_now
    sp.user_playlist_create(user_id, name, public=True, collaborative=False, description='A playlist of your top tracks, generated by ---')
    sp.user_playlist_add_tracks(user_id, name)

    #get user ID
    #offer to make playlist 
    #show options
    #allow name choice
    # make playlist 
    # add tracks
    #sp.user_playlist_create()
    return redirect(url_for('auth.home', _external=True))

def top_tracks(scale):
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    results = []
    iter = 0
    while True:
        offset = iter * 50
        iter += 1
        top_tracks = sp.current_user_top_tracks(limit=50, offset=offset,time_range=scale)
        for item in top_tracks["items"]:
            val = [item["name"]]
            val.append(item["artists"][0]["name"])
            results += [val]
        if (len(results)>99):
            break  
    df1 = pd.DataFrame(results, columns=["Song","Artists"])
    df1.index = df1.index + 1
    df = df1.reset_index().rename(columns={'index': '#'})
    return df