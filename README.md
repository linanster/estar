# estar
Energy Star query portal implementation

Start method:
1. python3 app.py
2. python3 wsgi.py
3. python4 manage.py runserver -h 0.0.0.0 -p 5000 -r -d
4. gunicorn --daemon --workers 4 --bind 0.0.0.0:5000 wsgi:application
5. run.sh --start/--stop
6. cp estar.service /usr/lib/systemd/system && 
   systemctl start estar.service
