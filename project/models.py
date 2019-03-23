"""
This module is for object relational mapping models.
"""
import uuid

import sentry_sdk
from flask import flash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import DBAPIError

from project import bcrypt

DB = SQLAlchemy()


def commit(alert_message=None, success_message=None):
    """
    Tries to commit the changes to the database, and handles errors.
    :param alert_message: message to flash on failure, defaults to exception message.
    :param success_message:  message to flash on success, defaults to None.
    :return: True
    """
    try:
        DB.session.commit()
        if success_message:
            flash(message=success_message, category="success")
        return True
    except DBAPIError as error:
        flash(message=alert_message or str(error), category="danger")
        sentry_sdk.capture_event(error)
        DB.session.rollback()
        return False


class BaseModel(DB.Model):
    """
    Our base model, all our other models inherit from this class, so we don't have to re implement
    common shared methods.
    """
    __abstract__ = True

    def store(self, alert_message=None, success_message=None):
        """
        Stores it self to the database
        :param alert_message: message to display on failure.
        :param success_message: message to display on success.
        :return: (boolean) True if operation succeeded otherwise False.
        """
        DB.session.add(self)
        return commit(alert_message, success_message)

    def remove(self, alert_message=None, success_message=None):
        """
        Removes it self from the database.
        :param alert_message: message to display on failure.
        :param success_message: message to display on success.
        :return: (boolean) True if operation succeeded otherwise False.
        """
        DB.session.delete(self)
        return commit(alert_message, success_message)


class User(BaseModel, UserMixin):
    """
    ORM model for the table "user"
    """
    __tablename__ = "user"
    email = DB.Column(DB.String, primary_key=True)
    admin = DB.Column(DB.Boolean, default=False)
    password = DB.Column(DB.String, nullable=False)

    def get_id(self):
        """
        Method needed for flask_login, since it by default expects the primary key to be called "id"
        if this method is not provided.
        :return: (string) email
        """
        return self.email

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password=password, rounds=10).decode('utf-8')
        self.admin = admin

    @classmethod
    def from_form(cls, form):
        """
        Initializes a user from a form.
        :param form: The form object which includes email and password fields.
        :return: an instance of User (calls User.__init__)
        """
        return cls(
            email=form.email.data.lower(),
            password=form.password.data.encode('utf-8')
        )


class Case(BaseModel):
    """
    ORM model for the table called "case".
    """
    __tablename__ = "case"
    id = DB.Column(UUID(as_uuid=True), primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    address = DB.Column(DB.String, nullable=False)
    date = DB.Column(DB.Date, nullable=False)
    show_on_page = DB.Column(DB.Boolean, default=True)

    def __init__(self, name, date, address):
        self.id = uuid.uuid4()
        self.name = name
        self.date = date
        self.address = address  # TODO verify address via google maps?

    @classmethod
    def from_form(cls, form):
        """
        Initializes a case from a form.
        :param form: The form object.
        :return: an instance of Case (calls Case.__init__)
        """
        return cls(
            name=form.case_name.data,
            date=form.case_date.data,
            address=form.case_address.data
        )

    def update(self, form):
        self.name = form.case_name.data,
        self.date = form.case_date.data,
        self.address = form.case_address.data
        return commit()


class Holiday(BaseModel):
    """
    ORM model for the table called "holiday".
    """
    __tablename__ = "holiday"
    id = DB.Column(UUID(as_uuid=True), primary_key=True)
    from_date = DB.Column(DB.Date)
    to_date = DB.Column(DB.Date)

    def __init__(self, from_date, to_date):
        self.id = uuid.uuid4()
        self.from_date = from_date
        self.to_date = to_date

    @classmethod
    def from_form(cls, form):
        """
        Initializes a holiday from a form.
        :param form: The form object which includes the fields from_date and to_date.
        :return: an instance of Holiday (calls Holiday.__init__)
        """
        return cls(
            from_date=form.from_date.data,
            to_date=form.to_date.data
        )
