from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from .utils import create_spotify_oauth, check_authorised, clean_cache

auth = Blueprint('auth', __name__)
TOKEN_INFO = 'token_info'

#this route loads the log in template and provides an authorisation URL via the create_spotify_Oauth function from utils

@auth.route('/login')
def login():
    clean_cache()
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return render_template('login.html', authorisation=auth_url)

#this route is where the user is directed once successfully logged in via spotify. It clears the session and obtains a new token for the session

@auth.route('/redir')
def redir():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    try:
        token_info = sp_oauth.get_access_token(code)
        session["token_info"] = token_info
        flash('You have successfully logged in', category='success')
    except:
        flash('Authentication failed. You may not have permissions to access website', category='error')
        flash('Please submit your email address for permission or use the test version', category='error')
        return redirect(url_for('views.home', _external=True))
    
    return redirect(url_for('views.home', _external=True))

#this function removes the session key and redirects the user to the log in page

@auth.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('auth.login'))
