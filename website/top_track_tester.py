from flask import Blueprint, session, redirect, render_template, flash, request
import pandas as pd

from .utils import get_token

top_track_tester = Blueprint('top_track_tester', __name__)

@top_track_tester.route('/top_test_short')
def top_test_short():
    session['token_info'], authorised = get_token()
    session.modified = True
    if not authorised:
        return redirect('/')
    specific = "(Short term)"
    header = "Top Tracks " + specific
    df = pd.read_csv('test_data/short_test.csv')
    flash('Successfully retrieved your top 100 Tracks'+header, category='Success')
    return render_template('top_tracks_table.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header, token_valid=authorised)

@top_track_tester.route('/top_test_medium')
def top_test_medium():
    session['token_info'], authorised = get_token()
    session.modified = True
    if not authorised:
        return redirect('/')
    specific = "(Medium term)"
    header = "Top Tracks " + specific
    df = pd.read_csv('test_data/medium_test.csv')
    flash('Successfully retrieved your top 100 Tracks'+header, category='Success')
    return render_template('top_tracks_table.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header, token_valid=authorised)

@top_track_tester.route('/top_test_long')
def top_test_long():
    session['token_info'], authorised = get_token()
    session.modified = True
    if not authorised:
        return redirect('/')
    specific = "(Long term)"
    header = "Top Tracks " + specific
    df = pd.read_csv('test_data/long_test.csv')
    flash('Successfully retrieved your top 100 Tracks'+header, category='Success')
    return render_template('top_tracks_table.html', table= df.to_html(classes='sortable', index=False, escape=False), title=header, token_valid=authorised)

