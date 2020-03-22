# estar
Energy Star query portal implementation

cd app
gunicorn --daemon -w 4 -b 10.30.30.101:5000 wsgi:application
--reload
--workers 4 --threads 1

