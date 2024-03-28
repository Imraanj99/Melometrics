from flask import Flask, url_for
from os import path
#import spotipy
#from spotipy import SpotifyOAuth



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'beans'
    
    from .auth import auth
    from .methods import methods
    from .views import views

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(methods, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    
    return app



