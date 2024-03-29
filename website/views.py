from flask import Blueprint, session, redirect, url_for, flash, render_template
import spotipy

from .utils import get_token, get_user

views = Blueprint('views', __name__)

# This defined the route for the home page

@views.route('/')
def home():
    session['token_info'], authorised = get_token()
    session.modified = True
    if not authorised:
        flash('Please log in', category='failure')
        return redirect(url_for('auth.login'))
    
    User = get_user()

    return render_template('home.html', name=User['display_name'])