import pytest

from flight_club import create_app


@pytest.fixture(scope="module")
def app():
    app = create_app()
    yield app


@pytest.fixture(scope="module")
def test_client(app):
    return app.test_client()
