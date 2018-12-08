from flask_babelplus import gettext
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField(label='email', validators=[DataRequired(), Email()])
    u = gettext("Password should minimum be 8 characters, and maximum 100 characters.")
    password = StringField(label='password', validators=[
        Length(min=8, max=100, message=u)]
    )
    remember = BooleanField(label='remember')

    def __repr__(self):
        return f"email: {self.email.data}\npassword: {self.password.data}\nremember: {self.remember.data}"


class CaseForm(FlaskForm):
    case_name = StringField(label='case_name', validators=[DataRequired()])
    case_date = StringField(label='case_date', validators=[DataRequired()])
