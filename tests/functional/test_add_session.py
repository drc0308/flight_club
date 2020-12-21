import pytest

from flight_club import db
from flight_club.models.models import User
from flight_club.sessions.views import session_input_validator, beer_input_validator
import flight_club.models.db_func as db_func
import datetime

from flask import g, session

@pytest.mark.parametrize(
    ("session_id", "date", "host", "result"),
    (
        ("2", "2020-01-01", "test", True),  # Correct input
        ("-1", "2020-01-01", "test", False),
        ("dog", "2020-01-01", "test", False),
        ("2", "not-a-date", "test", False),
        (
            "2",
            "10/12/2020",
            "test",
            False,
        ),  # This is the format we store but not what we expect
        ("2", "2020-01-01", "notauser", False),
    ),
)
def test_session_input_validator(app, session_id, date, host, result):
    with app.app_context():
        # Going to add a single session for supporting validation cases and a single user
        # TODO (dan) Later this can probably be a fixture of it's own
        db_func.add_session(1, "1/1/2020")
        db_func.add_user("test")
        val_result, error, session_object = session_input_validator(
            session_id, date, host
        )
        assert val_result == result
        if val_result:
            assert session_object.id == int(session_id)
            assert datetime.datetime.strptime(
                session_object.date, "%m/%d/%Y"
            ) == datetime.datetime.strptime(date, "%Y-%m-%d")


@pytest.mark.parametrize(
    (
        "beer_name",
        "beer_abv",
        "brewery",
        "style",
        "votes",
        "win",
        "username",
        "session_id",
        "result",
    ),
    (
        ("Good Beer", "2.1", "Good Brewery", "IPA", "1", "1", "test", "1", True), # Beer Name Cases
        ("", "2.1", "Good Brewery", "IPA", "1", "1", "test", "1", False),
        ("Good Beer", "2", "Good Brewery", "IPA", "1", "1", "test", "1", True), # ABV Cases
        ("Good Beer", "", "Good Brewery", "IPA", "1", "1", "test", "1", False),
        ("Good Beer", "-1", "Good Brewery", "IPA", "1", "1", "test", "1", False),
        ("Good Beer", "95.424", "Good Brewery", "IPA", "1", "1", "test", "1", True),
        ("Good Beer", "string", "Good Brewery", "IPA", "1", "1", "test", "1", False),
        ("Good Beer", "2.1", "", "IPA", "1", "1", "test", "1", False), # Brewery Cases
        ("Good Beer", "2.1", "Good Brewery", "", "", "1", "test", "1", False), #Style Cases
        ("Good Beer", "2.1", "Good Brewery", "IPA", "-1", "1", "test", "1", False), # Vote Cases
        ("Good Beer", "2.1", "Good Brewery", "IPA", "1.01", "1", "test", "1", False),
        ("Good Beer", "2.1", "Good Brewery", "IPA", "41", "1", "test", "1", True),
        ("Good Beer", "2.1", "Good Brewery", "IPA", "1", "0", "test", "1", True), # Win Cases
        ("Good Beer", "2.1", "Good Brewery", "IPA", "1", "-1", "test", "1", False),
        ("Good Beer", "2.1", "Good Brewery", "IPA", "1", "2", "test", "1", False),
        ("Good Beer", "2.1", "Good Brewery", "IPA", "1", "1", "notarealuser", "1", False), # User cases
    ),
)
def test_beer_input_validator(
    app, beer_name, beer_abv, brewery, style, votes, win, username, session_id, result
):
    with app.app_context():
        # The test user and session are added in test_session_input_validator
        # Need to make that a "module fixture"?
        val_result, error, session_object = beer_input_validator(
            beer_name, beer_abv, brewery, style, votes, win, username, session_id
        )
        assert val_result == result
