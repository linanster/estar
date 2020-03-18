from flask_login import LoginManager
from models import User

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def init_loginmanager(app):
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
