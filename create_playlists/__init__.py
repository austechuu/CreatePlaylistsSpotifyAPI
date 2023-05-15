# import the necessary modules
import os
from flask import Flask
# we'll import the blueprints we make a bit later right here.
from create_playlists.auth import auth_bp
from create_playlists.playlists import playlists_bp

# create an app instance
app = Flask(__name__)
# set the app secret
app.secret_key = os.urandom(24)


def create_app():
    # register blueprints with the app
    app.register_blueprint(auth_bp)
    app.register_blueprint(playlists_bp)

    # return the created app
    return app
