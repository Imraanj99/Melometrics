from flask import Blueprint, session, redirect, render_template, flash, url_for, request
import datetime
import spotipy
import pandas as pd

from .utils import get_token, get_image_path

methods = Blueprint('methods', __name__)

# this method returns a list the users liked songs (currently up to 150 due to restriction on number or requests to spotify api)
# once cleared by spotify to leave developer mode, this can be expanded to return the full list of liked songs

@methods.route('/get_tracks')
def get_all_tracks():

    #check if session valid and user still logged in

    session['token_info'], authorised = get_token()
    session.modified = True
    if not authorised:
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
    df0.index = df0.index + 1
    df3 = df0.reset_index().rename(columns={'index': '#'})
    #df3.index = df3.index + 1

    # Trim df to remove unnecessary columns and modify column headers
    # Turn duration from milliseconds to seconds and minutes

    df = df3.drop(['key','loudness','mode','liveness','type','id','uri','track_href','analysis_url','time_signature'],axis=1)
    df = df.rename(columns={'valence': 'Positivity', 'tempo': 'BPM','duration_ms':'Length'})
    df['BPM'] = df['BPM'].astype(int)
    def ms_to_min_sec(milliseconds):
        seconds = int((milliseconds / 1000) % 60)
        minutes = int(milliseconds / (1000 * 60))
        return f"{minutes}:{seconds:02d}"
    df['Length'] = df['Length'].apply(ms_to_min_sec)
    df[['danceability','energy','speechiness','acousticness','instrumentalness','Positivity']] = df[['danceability','energy','speechiness','acousticness','instrumentalness','Positivity']].applymap(get_image_path)

    # Output relevant information, convert df to html and redirect to table template

    #df.to_csv('songs.csv', index=False)
    header = "Liked songs"
    flash('Tracks retrieved successfully', category='success')
    return render_template('table.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header, token_valid=authorised)
    #return redirect(url_for('auth.home', _external=True))

# This uses the get_tracks function to retrieve top tracks over a short length of time 

@methods.route('/top_tracks_short')
def top_tracks_short():
    session['token_info'], authorised = get_token()
    session.modified = True
    if not authorised:
        return redirect('/')
    scale = 'short_term'
    specific = "(Short term)"
    df, success = top_tracks(scale, 100)
    if success:
        header = "Top Tracks " + specific
        flash('Successfully retrieved your top 100 Tracks'+header, category='Success')
        return render_template('top_tracks_table.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header, token_valid=authorised)
    else:
        return redirect(url_for('views.home', _external=True))


# This uses the get_tracks function to retrieve top tracks over a medium length of time 

@methods.route('/top_tracks_medium')
def top_tracks_medium():
    session['token_info'], authorised = get_token()
    session.modified = True
    if not authorised:
        return redirect('/')
    scale = 'medium_term'
    specific = "(Medium term)"
    df, success = top_tracks(scale, 100)
    if success:
        header = "Top Tracks " + specific
        flash('Successfully retrieved your top 100 Tracks'+header, category='Success')
        return render_template('top_tracks_table.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header, token_valid=authorised)
    else:
        return redirect(url_for('views.home', _external=True))



# This uses the get_tracks function to retrieve top tracks over a long length of time 

@methods.route('/top_tracks_long')
def top_tracks_long():
    session['token_info'], authorised = get_token()
    session.modified = True
    if not authorised:
        return redirect('/')

    scale = 'long_term'
    specific = "(Long term)"
    df, success = top_tracks(scale, 100)
    if success:
        header = "Top Tracks " + specific
        flash('Successfully retrieved your top 100 Tracks'+header, category='Success')
        return render_template('top_tracks_table.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header, token_valid=authorised)
    else:
        return redirect(url_for('views.home', _external=True))
    

# come back to this

@methods.route('/top_artists/<input_value>')
def top_artists(input_value):
    session['token_info'], authorised = get_token()
    session.modified = True
    if not authorised:
        return redirect('/')
    
    ranges = {'short_term':'Short Term', 'medium_term':'Medium Term', 'long_term':'Long Term'}
    if input_value not in ranges:
        flash('No such URL exists', category='failure')
        return redirect('/')
    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    results = []
    header = 'Top artists (' + ranges[input_value] + ')'

    top_artist = sp.current_user_top_artists(limit=50, offset=0,time_range=input_value)["items"]
    size = len(top_artist)
    if size == 0:
        flash('Insufficient listening data to create top artists', category='failure')
        return redirect('/')
    for item in top_artist:
        results += [item["name"]]
    print(len(results))
    df = pd.DataFrame(results, columns=["Artists"])
    df.index = df.index + 1
    df = df.reset_index().rename(columns={'index': '#'})
    flash('Top artists retrieved', category='success')
    return render_template('top_artist_table.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header, token_valid=authorised, number=size)




@methods.route('/make_playlist', methods=["POST", "GET"])
def make_playlist():
    session['token_info'], authorised = get_token()
    session.modified = True
    if not authorised:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    user_id = sp.current_user()['id']
    
    if request.method == 'POST':
        name = request.form.get('playlist_name')
        scale = request.form.get('selected_value')
        length = request.form.get('number_of_songs')

        if not name:
            current_date = datetime.datetime.now()
            date_now= current_date.strftime('%d-%m-%y')
            name = 'Top Tracks '+ date_now
        
        if len(name) > 100:
            flash('Playlist name must be less than 100 characters long', category='failure')
            return render_template('playlist_form.html')
    
        new_playlist = sp.user_playlist_create(user_id, name, public=True, collaborative=False, description='A playlist of your top tracks, generated by ---')
        new_playlist_id = new_playlist["id"]

        uris = top_track_uris(scale, length)
        print(len(uris))
        
        
        for i in range(0,len(uris),50):
            sp.playlist_add_items(new_playlist_id, uris[i:i+50])
        
        
        flash('Successfully created playlist', category='Success')
        return redirect(url_for('views.home'))

    return render_template('playlist_form.html', token_valid=authorised)

# generates a list of users top tracks based on 3 time scales 

def top_tracks(scale, length):
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    results = []
    iter = 0
    success = True

    while True:
        offset = iter * 50
        iter += 1
        top_tracks = sp.current_user_top_tracks(limit=50, offset=offset,time_range=scale)["items"]
        if not top_tracks:
            flash('Insufficient listening data to create top tracks', category='failure')
            success = False
            break
        for item in top_tracks:
            val = [item["name"]]
            val.append(item["artists"][0]["name"])
            results += [val]
            if len(results) >= int(length):
                break
        if (len(results)>(int(length)-1)):
            break  
    df1 = pd.DataFrame(results, columns=["Song","Artists"])
    df1.index = df1.index + 1
    df = df1.reset_index().rename(columns={'index': '#'})
    return df, success


def top_track_uris(scale, length):
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    results = []
    iter = 0
    while True:
        offset = iter * 50
        iter += 1
        top_tracks = sp.current_user_top_tracks(limit=50, offset=offset,time_range=scale)["items"]
        for item in top_tracks:
            val = [item["uri"]]
            results += val
        if (len(results)>(int(length)-1)):
            break  
    return results
