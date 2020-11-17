from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    account_source = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), unique=True, nullable=False)
    file_id = db.Column(db.String(120), unique=True, nullable=False)
    file_name = db.Column(db.String(80), unique=False, nullable=False)
    created_date = db.Column(db.DateTime, unique=False, nullable=False)
    update_date = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return '<File %r>' % self.file_name

