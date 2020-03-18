from flask import render_template, url_for, request, redirect
from flask import Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required

from models import User

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)

def init_views(app):
    app.register_blueprint(auth)
    app.register_blueprint(main)

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/about')
@login_required
def about():
    return render_template('about.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if user is not None:
        login_user(user)
        return redirect(url_for('main.index'))
    else:
        return render_template('login.html', msg="login failed!")


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
