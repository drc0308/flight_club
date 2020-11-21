import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import click

db = SQLAlchemy()

def create_app(test_config=None):
    """Create and configure the app
    """
    app = Flask(__name__, instance_relative_config=True)

    # some deploy systems set the database url in the environ
    db_url = os.environ.get("DATABASE_URL")

    if db_url is None:
        # default to a sqlite database in the instance folder
        db_url = "sqlite:///" + os.path.join(app.instance_path, "flight_club.sqlite")
        # ensure the instance folder exists
        os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # load instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder path exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello World!'
    
    # initialize Flask-SQLAlchemy and the init-db command
    db.init_app(app)
    app.cli.add_command(init_db_command)

    # Setup Flask Admin Panel
    admin = Admin(app, name='fightclub', template_mode='bootstrap3')
    from flight_club.models.models import User, Beer, Session
    from flight_club.admin.views import CsvView
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Beer, db.session))
    admin.add_view(ModelView(Session, db.session))
    admin.add_view(CsvView(name='CsvView', endpoint='csvview'))

    # Import blueprints
    from flight_club import auth
    from flight_club import sessions
    from flight_club import users
    app.register_blueprint(auth.bp)
    app.register_blueprint(sessions.bp)
    app.register_blueprint(users.bp)
    app.add_url_rule('/', endpoint='index')

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