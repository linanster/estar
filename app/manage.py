# coding:utf8
#
from flask_script import Manager
from app import create_app

app = create_app()

manager = Manager(app)

@manager.command
def createdb():
    from models import db, User
    db.create_all()
    User.seed()

@manager.command
def deletedb():
    from models import db
    db.drop_all()

if __name__ == '__main__':
    manager.run()

