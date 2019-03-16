from datetime import datetime

from flask import jsonify
from sqlalchemy import asc

from project.api import api
from project.models import DB, Case, Holiday


@api.route('/cases')
def cases():
    cases = DB.session.query(
        Case.id.label("id"),
        Case.date.label("date"),
        Case.name.label("name")
    ).filter(
        Case.date >= datetime.now()
    ).order_by(asc("date")).all()
    return jsonify(cases=cases)


@api.route("/holiday")
def holiday():
    """
    Checks if there's any planned holidays in the future.
    :return: (dict) JSON array of holidays.
    """

    holidays = Holiday.query.filter(
        Holiday.from_date >= datetime.now().date()
    ).all()

