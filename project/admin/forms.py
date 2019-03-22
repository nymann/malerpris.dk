"""
This module is used for forms used in /admin/*
"""
from flask_babelplus import gettext
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    """
    Form used for logging a user in.
    """
    email = StringField(label="email", validators=[DataRequired(), Email()])
    u = gettext("Password should minimum be 8 characters, and maximum 100 characters.")
    password = StringField(label="password", validators=[
        Length(min=8, max=100, message=u)]
                           )
    remember = BooleanField(label="remember")

    def __repr__(self):
        return f"email: {self.email.data}\n" \
            f"password: {self.password.data}\n" \
            f"remember: {self.remember.data}"


class CaseForm(FlaskForm):
    """
    Form for creating a case.
    """
    case_name = StringField(label="case_name", validators=[DataRequired()])
    case_date = StringField(label="case_date", validators=[DataRequired()])
    case_address = StringField(label="case_address", validators=[DataRequired()])


class HolidayForm(FlaskForm):
    """
    Form for going on holiday.
    """
    from_date = DateField(label="from_date")
    to_date = DateField(label="to_date")
    show_on_page = BooleanField(label="show_on_page")
