from datetime import timedelta

from flask import render_template, redirect, url_for, flash
from flask_babelex import gettext
from flask_login import login_required, login_user, logout_user

from project import bcrypt
from project.admin import admin
from project.forms import LoginForm, CaseForm
from project.models import User, Case


@admin.route("/", methods=['GET', 'POST'])
@login_required
def index():
    form = CaseForm()
    if form.validate_on_submit():
        case = Case(form=form)
        case.store()

    return render_template("admin/index.html", form=form)


@admin.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.get(email)
        password = form.password.data.encode('utf-8')
        if user and bcrypt.check_password_hash(pw_hash=user.password, password=password):
            login_user(user=user, remember=form.remember.data, duration=timedelta(days=30))
            e = gettext(u"logged in successfully!")
            flash(message=e, category="success")
            return redirect(url_for("admin.index"))
        else:
            e = gettext(u"User does not exist!")
            flash(message=e, category="danger")
    return render_template("admin/login.html", form=form)


@admin.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.index'))


@admin.route("/create_user", methods=["GET", "POST"])
def create_user():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.get(email)
        if user:
            e = gettext(u"User already exists!")
            flash(message=e, category="danger")
        else:
            user = User(form=form)
            user.store()
            e = gettext(u"User created.")
            flash(message=e, category="success")
            return redirect(url_for("admin.index"))
    return render_template("admin/create_user.html", form=form)
