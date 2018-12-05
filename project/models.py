from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    email = db.Column(db.String, primary_key=True)
    admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String, nullable=False)

    def get_id(self):
        return self.email


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)

