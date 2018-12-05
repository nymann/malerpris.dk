from flask import Blueprint

admin = Blueprint(
    name='admin',
    import_name=__name__,
    url_prefix='/admin',
    template_folder='templates'
)

from . import views