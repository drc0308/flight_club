import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import click

# TODO (dan) make a better system for loading in database csv contents on startup
TEST_CSV = "fc_test.csv"

db = SQLAlchemy()


def page_not_found(e):
    return render_template("404.html"), 404


def load_dev_db(app):
    with app.app_context():
        # TODO (dcuomo) load the test database on startup
        # Need to learn flask environment controls...
        import flight_club.models.db_func as db_func

        db_func.csv_add_filename(TEST_CSV)


def create_app(test_config=None):
    """Create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)
    app.register_error_handler(404, page_not_found)

    # (TODO) figure out how to like use flask config system
    import flight_club.fc_config as fc_config

    if os.getenv("FLASK_ENV") == "development":
        config_object = fc_config.DevConfig()
        app.config.from_object(config_object)
    else:
        # TODO still don't have good config management
        config_object = fc_config.Config()
        app.config.from_object(config_object)

    @app.route("/")
    def hello():
        return render_template("index.html")

    from flight_club.models.models import User, Beer, Session

    # Setup Flask Admin Panel
    admin = Admin(app, name="fightclub", template_mode="bootstrap3")
    from flight_club.admin.views import CsvView

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Beer, db.session))
    admin.add_view(ModelView(Session, db.session))
    admin.add_view(CsvView(name="CsvView", endpoint="csvview"))

    # Import blueprints
    from flight_club import auth
    from flight_club import sessions
    from flight_club import users

    app.register_blueprint(auth.bp)
    app.register_blueprint(sessions.bp)
    app.register_blueprint(users.bp)
    app.add_url_rule("/", endpoint="index")

    # initialize Flask-SQLAlchemy
    db.init_app(app)
    # TODO (dcuomo) this starts the database up every time fresh
    # I'll need to make this better later.
    with app.app_context():
        db.drop_all()
        db.create_all()

    try:
        if app.config["FLASK_ENV"] == "development":
            load_dev_db(app)
    except KeyError:
        pass

    return app

def get_app():
    return app

def init_db():
    db.drop_all()
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")
