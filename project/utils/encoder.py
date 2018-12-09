from datetime import datetime, date

from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.strftime("%d-%m-%Y")
            elif isinstance(obj, datetime):
                return obj.strftime("%d-%m-%Y %H:%M")
        except TypeError:
            pass

        return JSONEncoder.default(self, obj)
