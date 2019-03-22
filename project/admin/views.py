"""
This module is used for views (endpoints) prefixed with /admin
"""
from datetime import timedelta

from flask import render_template, redirect, url_for, flash
from flask_babelplus import gettext
from flask_login import login_required, login_user, logout_user

from project import bcrypt
from project.admin import admin
from project.admin.decorators import is_admin
from project.admin.forms import LoginForm, CaseForm, HolidayForm
from project.models import User, Case, Holiday


@admin.route("/", methods=['GET', 'POST'])
@login_required
@is_admin
def case():
    """
    Admin overview
    :return: renders HTML.
    """
    form = CaseForm()
    if form.validate_on_submit():
        case = Case.from_form(form=form)
        alert_message = gettext("Failed to add case.")
        success_message = gettext("Case added")
        case.store(alert_message=alert_message, success_message=success_message)

    return render_template("admin/case.html", form=form)


@admin.route("/login", methods=['GET', 'POST'])
def login():
    """
    Endpoint for admin user login.
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.get(email)
        password = form.password.data.encode('utf-8')
        if user and bcrypt.check_password_hash(pw_hash=user.password, password=password):
            login_user(user=user, remember=form.remember.data, duration=timedelta(days=30))
            error = gettext(u"logged in successfully!")
            flash(message=error, category="success")
            return redirect(url_for("site.index"))

        error = gettext(u"User does not exist!")
        flash(message=error, category="danger")
    return render_template("admin/login.html", form=form)


@admin.route("/logout")
@login_required
def logout():
    """
    Logs out a user
    :return:
    """
    logout_user()
    return redirect(url_for('site.index'))


@admin.route("/create_user", methods=["GET", "POST"])
@login_required
@is_admin
def create_user():
    """
    Creates a new user.
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.get(email)
        if user:
            error = gettext(u"User already exists!")
            flash(message=error, category="danger")
        else:
            user = User.from_form(form=form)
            user.store()
            error = gettext(u"User created.")
            flash(message=error, category="success")
            return redirect(url_for("site.index"))
    return render_template("admin/create_user.html", form=form)


@admin.route("/holiday", methods=["GET", "POST"])
def holiday():
    """
    Overview of holidays.
    :return:
    """
    form = HolidayForm()
    if form.validate_on_submit():
        holiday = Holiday.from_form(form=form)
        holiday.store()
        flash("Ferie oprettet.", category="success")
    return render_template("admin/holiday.html", form=form)
