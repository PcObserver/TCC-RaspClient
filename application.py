from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(**startup_config):

    app = Flask(__name__)
    app.config.from_pyfile("settings.py")
    app.config.update(startup_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("cade")
    from views import main_blueprint

    app.register_blueprint(main_blueprint)

    app.template_folder = "templates"

    return app
