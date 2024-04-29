from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5

db = SQLAlchemy()

from models import action, brand, device, user_device, user


def create_app(**startup_config):

    app = Flask(__name__)
    app.config.from_pyfile("settings.py")
    app.secret_key = app.config["SECRET_KEY"]
    app.config.update(startup_config)
    Bootstrap5(app)

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()
    from views import main_blueprint

    app.register_blueprint(main_blueprint)

    app.template_folder = "templates"

    return app