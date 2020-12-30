import pytest

from flight_club import db
from flask import g, session, json, jsonify
import flight_club.models.db_func as db_func


def test_beer_list_page_loads(test_client, app):
    with app.app_context():
        # Add a simple user and log in as user
        db_func.add_user("test", "test")
        test_client.post("/auth/login", data={"username": "test", "password": "test"})
        response = test_client.get("/beers/list")
        assert response.status_code == 200
