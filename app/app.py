#coding:utf8
#
from flask import Flask
from models import init_models
from views import init_views
from loginmanager import init_loginmanager
from bootstrap import init_bootstrap
import os


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    init_models(app)
    init_views(app)
    init_loginmanager(app)
    init_bootstrap(app)
    return app

app = create_app()

if __name__ == '__main__':
    appdir = os.path.abspath(os.path.dirname(__file__))
    topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    certfile = os.path.join(topdir,'cert/server.cert')
    keyfile = os.path.join(topdir,'cert/server.key')
    # app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True, ssl_context=(certfile, keyfile))
