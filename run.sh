#!/usr/bin/env sh
#
set -o errexit

TIMEOUT=30

if [ $# -eq 0 ]; then
    echo "run.sh [--start] [--stop] [--status] [--init]"
    exit 0
fi

workdir=$(cd "$(dirname $0)" && pwd)
cd "$workdir"

if [ "$1" == "--init" ]; then
    pip3 install virtualenv
    virtualenv venv
    source ./venv/bin/activate
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "==init config complete=="
        exit 0
    else
        echo "==init config fail=="
        exit 1
    fi
fi

if [ -d venv ]; then
    source ./venv/bin/activate
else
    echo "==venv error=="
    exit 1
fi

cd "$workdir/app"

if [ "$1" == '--start' ]; then
    # echo "gunicorn --daemon --workers 4 --bind 0.0.0.0:443 --keyfile ../cert/server.key --certfile ../cert/server.cert --timeout ${TIMEOUT} wsgi:application_ge_estar"
    # gunicorn --daemon --workers 4 --bind 0.0.0.0:443 --keyfile ../cert/server.key --certfile ../cert/server.cert --timeout "${TIMEOUT}" wsgi:application_ge_estar
    echo "gunicorn --daemon --workers 4 --bind 0.0.0.0:80  --timeout ${TIMEOUT} wsgi:application_ge_estar"
    gunicorn --daemon --workers 4 --bind 0.0.0.0:80 --timeout "${TIMEOUT}" wsgi:application_ge_estar
    sleep 1
    ps -ef | fgrep "gunicorn" | grep "application_ge_estar" | awk '{if($3==1) print $2}'
    exit 0
fi

if [ "$1" == "--stop" ]; then
    pid=$(ps -ef | fgrep "gunicorn" | grep "application_ge_estar" | awk '{if($3==1) print $2}')
    if [ "$pid" == "" ]; then
        echo "not running" 
    else
        echo "kill $pid"
        kill "$pid"
    fi
    exit 0
fi

if [ "$1" == "--status" ]; then
    pid=$(ps -ef | fgrep "gunicorn" | grep "application_ge_estar" | awk '{if($3==1) print $2}')
    echo "$pid"
    if [ "$pid" == "" ]; then
        echo "stopped" 
    else
        echo "started"
    fi
    exit 0
fi


