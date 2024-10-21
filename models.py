from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# 实例化SQLAlchemy
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Function(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(150), unique=True, nullable=False)
    function_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))

class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(150), unique=True, nullable=False)
