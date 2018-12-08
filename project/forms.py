from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField(label='email', validators=[DataRequired(), Email()])
    password = StringField(label='password', validators=[
        Length(min=8, max=100, message="Password should minimum be 8 characters, and maximum 100 characters.")]
    )
    remember = BooleanField(label='remember')

    def __repr__(self):
        return f"email: {self.email.data}\npassword: {self.password.data}\nremember: {self.remember.data}"
