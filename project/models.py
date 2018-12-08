from flask import flash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from project import bcrypt

db = SQLAlchemy()


class User(db.Model, UserMixin):
    email = db.Column(db.String, primary_key=True)
    admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String, nullable=False)

    def get_id(self):
        return self.email

    def __init__(self, form):
        self.email = form.email.data.lower()
        password = form.password.data.encode('utf-8')
        self.password = bcrypt.generate_password_hash(password=password, rounds=10).decode('utf-8')
        self.admin = False

    def store(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            flash("A user with that email already exists.")
            db.session.rollback()
        except SQLAlchemyError as e:
            # This should just throw the 500 internal server error.
            db.session.rollback()


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
