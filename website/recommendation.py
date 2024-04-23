from flask import Blueprint, session, redirect, render_template, flash, url_for, request
import spotipy
import pandas as pd

from .utils import get_token, check_authorised, get_user, get_image_path

recommendations = Blueprint('recommendations', __name__)

@recommendations.route('/recommended_artists', methods=["POST", "GET"])
def recommended_artists():
    session['token_info'], authorised = get_token()
    session.modified = True
    if not authorised:
        return redirect('/')
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
