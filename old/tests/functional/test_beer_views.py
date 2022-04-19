import pytest

from flask import g, session, json, jsonify
from flight_club import db
from flight_club.beers.views import return_sorted_beers
import flight_club.models.db_func as db_func


@pytest.fixture(scope="module")
def beer_list_app(app):
    with app.app_context():
        # Add a simple user and log in as user
        db_func.add_user("test", "test")
        db_func.add_user("other", "test")

        # Add a fake session for the sort tests
        db_func.add_session(1, "1/1/2020")
        db_func.add_session(2, "2/1/2020")

        # Add a few beers for the sort tests
        db_func.add_beer(
            ["1", "", "test", "", "A Beer", "B Brewery", "1", "0", "", "IPA", "6.1"]
        )
        db_func.add_beer(
            ["1", "", "other", "", "B Beer", "C Brewery", "2", "1", "", "Lager", "4.2"]
        )
        db_func.add_beer(
            ["2", "", "test", "", "C Beer", "A Brewery", "3", "1", "", "Stout", "6.2"]
        )

    yield app


def test_beer_list_page_loads(test_client, beer_list_app):
    with beer_list_app.app_context():
        test_client.post("/auth/login", data={"username": "test", "password": "test"})
        response = test_client.get("/beers/list")
        assert response.status_code == 200


def test_beer_list_sort_cases(test_client, beer_list_app):
    with beer_list_app.app_context():

        beer_list = return_sorted_beers(key="beer_name", sort="asc")
        assert beer_list[0].beer_name == "A Beer"
        assert beer_list[1].beer_name == "B Beer"
        assert beer_list[2].beer_name == "C Beer"

        beer_list = return_sorted_beers(key="beer_name", sort="desc")
        assert beer_list[0].beer_name == "C Beer"
        assert beer_list[1].beer_name == "B Beer"
        assert beer_list[2].beer_name == "A Beer"

        beer_list = return_sorted_beers(key=None, sort=None)
        assert beer_list[0].beer_name == "A Beer"
        assert beer_list[1].beer_name == "B Beer"
        assert beer_list[2].beer_name == "C Beer"


def test_beer_list_page_loads_with_sorts(test_client, beer_list_app):
    with beer_list_app.app_context():
        test_client.post("/auth/login", data={"username": "test", "password": "test"})
        response = test_client.get("/beers/list?key=beer_name&sort=asc")
        assert response.status_code == 200
