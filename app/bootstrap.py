from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

def init_bootstrap(app):
    bootstrap.init_app(app)
