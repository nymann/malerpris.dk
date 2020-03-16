import sentry_sdk
from flask import Flask
from flask_babelplus import Babel, gettext
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from project.error_handlers import register_handlers
from project.utils.encoder import CustomJSONEncoder

login_manager = LoginManager()
login_manager.login_view = "admin.login"
babel = Babel()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    app.config.from_object(Config)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    initialize_extensions(app=app)
    register_blueprints(app=app)
    register_handlers(app=app)
    return app


def initialize_extensions(app):
    # Database
    from project.models import DB
    DB.init_app(app=app)
    with app.app_context():
        DB.create_all(app=app)

    # Flask Migrate
    migrate.init_app(app=app, db=DB)

    # Babel
    babel.init_app(app=app)

    @babel.localeselector
    def get_locale():
        return "da"

    # Login
    login_manager.login_message = gettext("You need to be authenticated to visit that page.")
    login_manager.login_message_category = "info"
    login_manager.init_app(app=app)
    from project.models import User

    @login_manager.user_loader
    def user_loader(email):
        return User.query.get(email)

    bcrypt.init_app(app=app)

    # Sentry
    sentry_sdk.init(
        integrations=[FlaskIntegration()],
        release="1.0.1"
    )


def register_blueprints(app):
    from project.admin import admin
    app.register_blueprint(admin)

    from project.site import site
    app.register_blueprint(site)

    from project.api import api
    app.register_blueprint(api)
