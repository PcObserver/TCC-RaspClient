from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_htmx import HTMX
from api.api_adapter import ApiAdapter

api = ApiAdapter()
db = SQLAlchemy()
htmx = HTMX()

from models import action, author, brand, device, user_device
from views import (
    application_blueprint,
    device_blueprint,
    brand_blueprint,
    user_device_blueprint,
    action_blueprint,
    auth_blueprint,
)


def create_app(**startup_config):

    app = Flask(__name__)
    app.config.from_pyfile("settings.py")
    app.secret_key = app.config["SECRET_KEY"]
    app.config.update(startup_config)

    htmx.init_app(app)
    db.init_app(app)
    api.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()

    app.register_blueprint(application_blueprint)
    app.register_blueprint(device_blueprint)
    app.register_blueprint(brand_blueprint)
    app.register_blueprint(user_device_blueprint)
    app.register_blueprint(action_blueprint)
    app.register_blueprint(auth_blueprint)

    app.template_folder = "templates"

    @app.after_request
    def render_messages(response: Response) -> Response:
        if (
            request.headers.get("HX-Request")
            and response.data.find(b'div id="alerts"') == -1
        ):
            messages = render_template("components/alerts.html")
            response.data = response.data + messages.encode("utf-8")
        return response

    return app
