#!/usr/bin/env sh
#
workdir=$(cd "$(dirname $0)" && pwd)
cd "$workdir"

if [ "$1" == '--start' ]; then
    echo "gunicorn --daemon --workers 4 --bind 0.0.0.0:5000 wsgi:application"
    gunicorn --daemon --workers 4 --bind 0.0.0.0:5000 wsgi:application
    ps -ef | fgrep "gunicorn" | grep "application" | awk '{if($3==1) print $2}'
    exit 0
fi

if [ "$1" == "--stop" ]; then
    pid=$(ps -ef | fgrep "gunicorn" | grep "application" | awk '{if($3==1) print $2}')
    if [ "$pid" == "" ]; then
        echo "not running" 
    else
        echo "kill $pid"
        kill "$pid"
    fi
    exit 0
fi

if [ "$1" == "--status" ]; then
    pid=$(ps -ef | fgrep "gunicorn" | grep "application" | awk '{if($3==1) print $2}')
    echo "$pid"
    if [ "$pid" == "" ]; then
        echo "stopped" 
    else
        echo "started"
    fi
    exit 0
fi

echo "run.sh [--start] [--stop] [--status]"

