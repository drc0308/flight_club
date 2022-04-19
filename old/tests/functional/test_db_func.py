import pytest

from flight_club import db
import flight_club.models.db_func as db_func


def test_no_user_check(app, test_client):
    # This database should be empty at the start.
    with app.app_context():
        assert db_func.check_if_user_exists("test") == False


def test_add_user(app, test_client):
    # Test adding a user
    with app.app_context():
        db_func.add_user("test", "test")
        assert db_func.check_if_user_exists("test") == True


def test_no_session_check(app, test_client):
    # This database should be empty at the start.
    with app.app_context():
        assert db_func.check_if_session_exists(1) == False


def test_add_session(app, test_client):
    with app.app_context():
        db_func.add_session(1, "1/1/2020")
        assert db_func.check_if_session_exists(1) == True


def test_add_beer(app, test_client):
    with app.app_context():
        # TODO right now this is an annoying csv row
        beer = []
        beer.append(str(1))  # 0 - Session ID string
        beer.append("")  # 1 - Unused
        beer.append("test")  # 2 - Username
        beer.append("")  # 3 - Unused
        beer.append("Cool Beer Name")  # 4 - beername
        beer.append("Hip Brewery")  # 5 - brewery
        beer.append(str(2))  # 6 - votes
        beer.append(str(1))  # 7 - win
        beer.append("")  # 8 - unused
        beer.append("IPA")  # 9 - style
        beer.append(str(6.12))  # 10 - abv

        db_func.add_beer(beer)

        # Query Database for Beer
        res_beer = db_func.get_beer("Cool Beer Name")
        assert len(res_beer) == 1
        assert res_beer[0].id == 1
        assert res_beer[0].beer_name == "Cool Beer Name"
        assert res_beer[0].brewery == "Hip Brewery"
        assert res_beer[0].style == "IPA"
        assert res_beer[0].votes == 2
        assert res_beer[0].win == 1
        assert res_beer[0].username == "test"
        assert res_beer[0].session_id == 1
