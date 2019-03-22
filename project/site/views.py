from datetime import datetime

from flask import render_template
from sqlalchemy import asc

from project.models import DB, Case, Holiday
from project.site import site


@site.route('/')
def index():
    compare_date = datetime.now()

    cases = DB.session.query(
        Case.id.label("id"),
        Case.date.label("date"),
        Case.name.label("name"),
        Case.address.label("address")
    ).filter(
        Case.date >= compare_date
    ).order_by(asc("date")).all()

    holiday = Holiday.query.filter(
        Holiday.to_date > compare_date.date()
    ).order_by(Holiday.to_date.asc()).first()

    return render_template('site/index.html', cases=cases, holiday=holiday)


@site.route('/error')
def error():
    return render_template('errors/internal_server_error.html')
