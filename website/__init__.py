from flask import Flask, url_for
from os import path
import spotipy
from spotipy import SpotifyOAuth



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'beans'
    
    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')
    
    return app



