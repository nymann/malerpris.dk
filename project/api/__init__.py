from flask import Blueprint

api = Blueprint(
    name='api',
    import_name=__name__,
    url_prefix='/api',
    template_folder='templates'
)

from . import views