from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_htmx import HTMX
from utils.api_adapter import ApiAdapter

api = ApiAdapter()
db = SQLAlchemy()
htmx = HTMX()

from models import action, brand, device, user_device, user
from views import application_blueprint, device_blueprint, brand_blueprint, user_device_blueprint, action_blueprint, signals_blueprint, auth_blueprint

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
    app.register_blueprint(signals_blueprint)
    app.register_blueprint(auth_blueprint)

    app.template_folder = "templates"

    return app
