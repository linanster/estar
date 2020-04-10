SECRET_KEY = "EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA"
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///secret.sqlite3'
Debug = True
TypeRestrict = True



import os
topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
logfolder = os.path.abspath(os.path.join(topdir, "log"))
