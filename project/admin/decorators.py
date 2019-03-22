import functools

from flask import flash, redirect, url_for
from flask_babelplus import gettext
from flask_login import current_user


def is_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            t = gettext("You need to be authenticated and an admin to access that page.")
            flash(t, "danger")
            return redirect(url_for('admin.login'))
        if not current_user.admin:
            t = gettext("Only admin users can access that page, contact the administrator.")
            flash(t, "danger")
            return redirect(url_for('site.index'))
        return func(*args, **kwargs)

    return wrapper
