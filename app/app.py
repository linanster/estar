#coding:utf8
#
from flask import Flask
from models import init_models
from views import init_views
from loginmanager import init_loginmanager
from bootstrap import init_bootstrap

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
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
