from flask import Blueprint, render_template, flash, redirect
import pandas as pd

# This file is a temporary file which exists to provide an example of app functionality to individuals who do not have permisssions to access the site via O-Auth using their own spotify account
# This file will be removed once the "extended quota request" is approved by spotify which will allow anyone with a spotifyu account to access the site

tester = Blueprint('tester', __name__)

# This defined the route for the test home page

@tester.route('/home')
def test_home():
    return render_template('test_templates/test_home.html')

# test liked songs

@tester.route('/liked_songs')
def test_songs():
    df = pd.read_csv('test_data/songs_test.csv')
    header = 'Liked song analysis (test)'
    size = '150'
    return render_template('test_templates/song_analysis_test_table.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header, number=size)

# test top tracks with 3 time lengths

@tester.route('/top_tracks/<input_value>')
def test_top_tracks(input_value):
    ranges = {'short_term':'Short Term', 'medium_term':'Medium Term', 'long_term':'Long Term'}
    if input_value not in ranges:
        flash('No such URL exists', category='failure')
        return redirect('/test/home')
    
    df = pd.read_csv(f"test_data/{str(input_value).split('_')[0]}_test.csv")
    header = 'Top Tracks (' + ranges[input_value] + ')'

    
    size = len(df)
    flash('Top (test) Tracks retrieved', category='success')
    return render_template('test_templates/top_test_table.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header, number=size)

# audio analysis of (test) top tracks

@tester.route('/top_features/<input_value>')
def test_top_track_features(input_value):
    ranges = {'short_term':'Short Term', 'medium_term':'Medium Term', 'long_term':'Long Term'}
    if input_value not in ranges:
        flash('No such URL exists', category='failure')
        return redirect('/test/home')
    
    df = pd.read_csv(f"test_data/{str(input_value).split('_')[0]}_test_features.csv")
    header = 'Top Tracks (' + ranges[input_value] + ')(test)'

    return render_template('test_templates/top_test_features_table.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header)

# top (test) artists over 3 time scales

@tester.route('/top_artists/<input_value>')
def test_artists(input_value):
    ranges = {'short_term':'Short Term', 'medium_term':'Medium Term', 'long_term':'Long Term'}
    if input_value not in ranges:
        flash('No such URL exists', category='failure')
        return redirect('/test/home')
    
    df = pd.read_csv(f"test_data/test_artist_{str(input_value).split('_')[0]}.csv")
    header = 'Top artists (' + ranges[input_value] + ')'

    size = len(df)
    flash('Top artists (test) retrieved', category='success')
    return render_template('test_templates/test_artist_table.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header, number=size)

@tester.route('/make_playlist')
def test_makke_playlist():

    return render_template('test_templates/test_form.html')

# displays an image of a created playlist

@tester.route('example_playlist')
def example_playlist():
    return render_template('test_templates/example_playlist.html')

# a duplicate of the about page which uses the test version base template
# this preserves the test option in the navbar to prevent the use being returned to log in page for not being signed in

@tester.route('about')
def about():
    return render_template('test_templates/test_about.html')

# a duplicate of the feature info page which uses the test version base template

@tester.route('feature_info')
def feature_info():
    return render_template('test_templates/test_feature_info.html')

# placeholder route to redirect to test home page if in dev feature accessed

@tester.route('recommendations')
def recommendations():
    flash('This feature is currently in development, please come back soon', category='failure')
    return redirect('/test/home')