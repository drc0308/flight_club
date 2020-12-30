import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base config."""

    # This should probably not be hardcoded?
    # What is this for again lol?
    FLASK_ENV = "test"
    SECRET_KEY = "dev"
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 20

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return os.getenv("DATABASE_URL", "sqlite://")


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
