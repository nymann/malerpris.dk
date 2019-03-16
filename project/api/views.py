from datetime import datetime

from flask import jsonify
from sqlalchemy import asc

from project.api import api
from project.models import DB, Case, Holiday


@api.route("/holiday")
def holiday():
    """
    Checks if there's any planned holidays in the future.
    :return: (dict) JSON array of holidays.
    """

    holidays = Holiday.query.filter(
        Holiday.from_date >= datetime.now().date()
    ).all()

