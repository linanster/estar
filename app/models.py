from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy(use_native_unicode='utf8')

def init_models(app):
    db.init_app(app)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    def __init__(self, username, password, description=''):
        self.username = username
        self.password = password
        self.description = description
    @staticmethod
    def seed():
        user_1 = User('user1', '123456')
        user_2 = User('estar', 'cbyge')
        db.session.add_all([user_1, user_2])
        db.session.commit()
