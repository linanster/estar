from app import create_app
import os

application = create_app()

if __name__ == '__main__':
    appdir = os.path.abspath(os.path.dirname(__file__))
    topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    certfile = os.path.join(topdir,'cert/server.cert')
    keyfile = os.path.join(topdir,'cert/server.key')
    application.run(host='0.0.0.0', port=5000, debug=True, threaded=True, ssl_context=(certfile, keyfile))
