from flask import render_template, url_for, request, redirect, send_from_directory
from flask import Blueprint
from flask_login import login_user, logout_user, login_required
import os

from models import User
from mylib import get_consumption, get_power, get_all
from settings import Debug
from settings import logfolder
from mydecorator import viewfunclog
from mylogger import logger

# Debug = True

auth = Blueprint('auth', __name__, url_prefix='/estar')
main = Blueprint('main', __name__, url_prefix='/estar')

def init_views(app):
    app.register_blueprint(auth)
    app.register_blueprint(main)

@main.route('/')
@main.route('/index')
@login_required
@viewfunclog
def index():
    return render_template('index.html', new=1)

@main.route('/query', methods=['GET', 'POST'])
@login_required
@viewfunclog
def query():
    if request.method == 'GET':
        return redirect(url_for('main.index'))
    mac_input = request.form.get('mac')
    logger.info('==mac_input=={}'.format(mac_input))

    # version 1
    # pass mac from page to xlink api without no changes
    # mac = transform(mac_input)
    # consumption_j, consumption_kwh, power_watt, errno, errmsg = get_all(mac)

    # version 2
    # gen 4 macs from mac_input, and try one by one when encounter DeviceNotFound response
    macs = gen_4_macs(mac_input)
    index = 1
    logger.info('==macs=={}'.format(macs))
    for mac in macs:
        logger.info('==try mac({})=={}'.format(index, mac))
        consumption_j, consumption_kwh, power_watt, errno, errmsg = get_all(mac)
        logger.info('==errno=={}'.format(errno))
        index += 1
        # if errno != 0:
        if errno == -3:
            continue
        else:
            break
    # end version 2
     
    logger.info('==mac=={}'.format(mac))
    logger.info('==consumption_j=={}'.format(consumption_j))
    logger.info('==consumption_kwh=={}'.format(consumption_kwh))
    logger.info('==power_watt=={}'.format(power_watt))
    logger.info('==errno=={}'.format(errno))
    logger.info('==errmsg=={}'.format(errmsg))
    logger.info('')
    params = {"mac_input":mac_input, "consumption_j":consumption_j, "consumption_kwh":consumption_kwh, "power_watt":power_watt, "errno":errno, "errmsg":errmsg, "query":True}
    return render_template('index.html', **params)

@auth.route('/login', methods=['GET', 'POST'])
@viewfunclog
def login():
    logger.warn('client from {}'.format(request.remote_addr))
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

@main.route('/about')
@login_required
@viewfunclog
def about():
    return render_template('about.html')

@main.route('/log')
@login_required
@viewfunclog
def log():
    filelist = os.listdir(logfolder)
    return render_template('log.html', filelist=filelist)

@main.route('/logview')
@viewfunclog
def cmd_logview():
    filename = request.args.get('filename')
    return send_from_directory(logfolder, filename, as_attachment=False)

@main.route('/download')
@viewfunclog
def cmd_logdownload():
    filename = request.args.get('filename')
    return send_from_directory(logfolder, filename, as_attachment=True)

@auth.route('/logout')
@viewfunclog
def logout():
    logout_user()
    return redirect(url_for('main.index'))

def transform(mac):
# mac format on App side: "A4:C1:38:6D:40:1D"
# mac format on database side: "1D406D38C1A4"
    # mac_list = mac.split(':')
    # mac_list.reverse()
    # mac_new = "".join(mac_list)
    # case sensitive
    # return mac_new.upper()
    return mac

def gen_4_macs(mac):
    mac_upper = mac.upper()
    mac_lower = mac.lower()
    mac_upper_reverse = reverse_mac(mac_upper)
    mac_lower_reverse = reverse_mac(mac_lower)
    macs = list()
    macs.append(mac_lower)
    macs.append(mac_upper)
    macs.append(mac_lower_reverse)
    macs.append(mac_upper_reverse)
    return macs

def split_per_2(mystr):
    index = 0
    mylist = list()
    for letter in mystr:
        if index%2 == 0:
            seg = letter
        else:
            seg = seg + letter
            mylist.append(seg)
        index += 1
    return mylist

def reverse_mac(mac):
    mac_list = split_per_2(mac)
    mac_list.reverse()
    mac_reverse = "".join(mac_list)
    return mac_reverse
        
