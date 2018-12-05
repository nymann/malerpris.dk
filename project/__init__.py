from flask import Flask
from flask_babelex import Babel
from flask_login import LoginManager
from sentry_sdk.integrations.flask import FlaskIntegration

from config import Config
from project.error_handlers import register_handlers

import sentry_sdk

login_manager = LoginManager()
login_manager.login_view = "admin.login"
babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    initialize_extensions(app=app)
    register_blueprints(app=app)
    register_handlers(app=app)
    return app


def initialize_extensions(app):
    from project.models import db
    db.init_app(app=app)
    with app.app_context():
        db.create_all(app=app)
    login_manager.init_app(app=app)
    from project.models import User

    @login_manager.user_loader
    def user_loader(email):
        return User.query.get(email)

    babel.init_app(app=app)
    sentry_sdk.init(
        integrations=[FlaskIntegration()],
        release="1.0.0"
    )


def register_blueprints(app):
    from project.admin import admin
    from project.site import site

    app.register_blueprint(admin)
    app.register_blueprint(site)
