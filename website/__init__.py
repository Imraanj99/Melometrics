from flask import Flask, url_for
from os import path
from secret_info import secret_key

# This function creates a Flask application and secret key. it also imports the routes and blueprints

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    
    from .auth import auth
    from .methods import methods
    from .views import views

    # route for the test account as it does not have 1 year of data from which to generate top tracks
    from .top_track_tester import top_track_tester

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(methods, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(top_track_tester, url_prefix='/')
    
    return app





