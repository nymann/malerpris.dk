from flask import Flask, request
from flask_babelplus import Babel, gettext
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from sentry_sdk.integrations.flask import FlaskIntegration

from config import Config
from project.error_handlers import register_handlers

import sentry_sdk

from project.utils.encoder import CustomJSONEncoder

login_manager = LoginManager()
login_manager.login_view = "admin.login"
babel = Babel()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    app.config.from_object(Config)
    initialize_extensions(app=app)
    register_blueprints(app=app)
    register_handlers(app=app)
    return app


def initialize_extensions(app):
    # Database
    from project.models import db
    db.init_app(app=app)
    with app.app_context():
        db.create_all(app=app)

    # Babel
    babel.init_app(app=app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(['da', 'en'])

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
        release="1.0.0"
    )


def register_blueprints(app):
    from project.admin import admin
    app.register_blueprint(admin)

    from project.site import site
    app.register_blueprint(site)

    from project.api import api
    app.register_blueprint(api)
