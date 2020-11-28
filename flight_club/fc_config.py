import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base config."""
    # This should probably not be hardcoded?
    # What is this for again lol?
    SECRET_KEY = 'dev'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        instance_path = basedir + "/instance/"
        try:
            print(basedir)
            os.makedirs(instance_path, exist_ok=True)
        except OSError:
            pass
        return "sqlite:///" + os.path.join(instance_path, "flight_club.sqlite")

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True