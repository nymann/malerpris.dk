from datetime import datetime

from flask import render_template
from sqlalchemy import asc

from project.models import DB, Case
from project.site import site


@site.route('/')
def index():
    cases = DB.session.query(
        Case.id.label("id"),
        Case.date.label("date"),
        Case.name.label("name")
    ).filter(
        Case.date >= datetime.now()
    ).order_by(asc("date")).all()
    return render_template('site/index.html', cases=cases)


@site.route('/error')
def error():
    return render_template('errors/internal_server_error.html')
