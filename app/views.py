from flask import render_template, url_for, request, redirect
from flask import Blueprint
from flask_login import login_user, logout_user, login_required

from models import User
from mylib import get_consumption

Debug = True

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)

def init_views(app):
    app.register_blueprint(auth)
    app.register_blueprint(main)

@main.route('/')
@main.route('/index')
@login_required
def index():
    return render_template('index.html')

@main.route('/query', methods=['GET', 'POST'])
@login_required
def query():
    if request.method == 'GET':
        return redirect(url_for('main.index'))
    mac = request.form.get('mac')
    consumption, errno, errmsg = get_consumption(mac)
    consumption_kwh = consumption/(1000*3600)
    if Debug:
        print('==mac==', mac)
        print('==consumption==', consumption)
        print('==errno==', errno)
        print('==errmsg==', errmsg)
        print('==consumption_kwh==', consumption_kwh)
    if errno == -1:
        # exposing original error message to user is not friendly
        return render_template('index.html', errmsg='unknown error')
    if errno == -2:
        return render_template('index.html', errmsg=errmsg)
    return render_template('index.html', consumption=consumption, consumption_kwh=consumption_kwh)

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
        return render_template('login.html', warning="login failed!")


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
