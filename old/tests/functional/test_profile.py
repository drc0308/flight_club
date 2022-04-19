import pytest

from flight_club import db
from flight_club.users.fc_member import FCMember

from flask import g, session, json, jsonify
import flight_club.models.db_func as db_func


def test_new_user_object(test_client, app):
    with app.app_context():
        # Add a simple user
        db_func.add_user("test", "test")
        new_user = FCMember("test")
        assert new_user.username == "test"
        assert new_user.win_count == 0
        assert not new_user.beers
        assert not new_user.wins
        assert new_user.avg_score == 0.0
        assert new_user.avg_abv == 0.0


def test_new_user_page(test_client, app):
    with app.app_context():
        response = test_client.get("/users/test")
        assert response.status_code == 200
