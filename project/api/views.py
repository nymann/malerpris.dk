from datetime import datetime

from flask import jsonify
from sqlalchemy import asc

from project.api import api
from project.models import db, Case


@api.route('/cases')
def cases():
    cases = db.session.query(
        Case.id.label("id"),
        Case.date.label("date"),
        Case.name.label("name")
    ).filter(
        Case.date >= datetime.now()
    ).order_by(asc("date")).all()
    return jsonify(cases=cases)
