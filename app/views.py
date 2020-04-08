from flask import render_template, url_for, request, redirect
from flask import Blueprint
from flask_login import login_user, logout_user, login_required

from models import User
from mylib import get_consumption, get_power, get_all
from settings import Debug

# Debug = True

auth = Blueprint('auth', __name__, url_prefix='/estar')
main = Blueprint('main', __name__, url_prefix='/estar')

def init_views(app):
    app.register_blueprint(auth)
    app.register_blueprint(main)

@main.route('/')
@main.route('/index')
@login_required
def index():
    return render_template('index.html', new=1)

@main.route('/query', methods=['GET', 'POST'])
@login_required
def query():
    if request.method == 'GET':
        return redirect(url_for('main.index'))
    mac = request.form.get('mac')
    mac = transform(mac)
    # consumption_j, consumption_kwh, errno, errmsg = get_consumption(mac)
    # power_watt = get_power(mac)
    consumption_j, consumption_kwh, power_watt, errno, errmsg = get_all(mac)
     
    if Debug:
        print('==mac==', mac)
        print('==consumption_j==', consumption_j)
        print('==consumption_kwh==', consumption_kwh)
        print('==power_watt==', power_watt)
        print('==errno==', errno)
        print('==errmsg==', errmsg)
        print('')
    params = {"consumption_j":consumption_j, "consumption_kwh":consumption_kwh, "power_watt":power_watt, "errno":errno, "errmsg":errmsg, "query":True}
    return render_template('index.html', **params)

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

def transform(mac):
# mac format on App side: "A4:C1:38:6D:40:1D"
# mac format on database side: "1D406D38C1A4"
    mac_list = mac.split(':')
    mac_list.reverse()
    mac_new = "".join(mac_list)
    # case sensitive
    return mac_new.upper()
