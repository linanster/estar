from flask import Flask
from models import init_models
from views import init_views
from loginmanager import init_loginmanager

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    init_models(app)
    init_views(app)
    init_loginmanager(app)
    return app
