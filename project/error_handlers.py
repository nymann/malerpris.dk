import sentry_sdk
from flask import render_template


def register_handlers(app):
    # if app.config.get("DEBUG") is True:
    #     app.logger.debug("Skipping error handlers in debug mode.")
    #     return

    @app.errorhandler(404)
    def page_not_found(e):
        sentry_sdk.capture_message(f"{e.code}: {e.description}")
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        # sentry_sdk.capture_message(f"{e.code}: {e.description}")
        return render_template("errors/internal_server_error.html"), 500
