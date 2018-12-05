from flask import Blueprint

site = Blueprint(
    name='site',
    import_name=__name__,
    url_prefix='',
    template_folder='templates'
)

from . import views