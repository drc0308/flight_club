import pytest

from flight_club import db
from flight_club.models.models import User, Beer
from flight_club.sessions.views import AddSessionFormValidator, ValidatorResults
import flight_club.models.db_func as db_func
import datetime

from flask import g, session


def build_session_request_dict(session_id, date, host):
    return {"session_id": session_id, "date": date, "host": host}


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
        db_func.add_user("test", "test")

        request = build_session_request_dict(session_id, date, host)
        validator = AddSessionFormValidator(request)

        val_result = validator.validate_session()

        assert val_result.success == result
        if val_result.success:
            assert validator.session_model.id == int(session_id)
            assert datetime.datetime.strptime(
                validator.session_model.date, "%m/%d/%Y"
            ) == datetime.datetime.strptime(date, "%Y-%m-%d")


def build_beer_request_dict(
    beer_name, beer_abv, brewery, style, votes, win, username, id
):
    return {
        "beer_{}".format(id): beer_name,
        "beer_abv_{}".format(id): beer_abv,
        "brewery_{}".format(id): brewery,
        "style_{}".format(id): style,
        "votes_{}".format(id): votes,
        "win_{}".format(id): win,
        "username_{}".format(id): username,
    }


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
        (
            "Good Beer",
            "2.1",
            "Good Brewery",
            "IPA",
            "1",
            "1",
            "test",
            "1",
            True,
        ),  # Beer Name Cases
        ("", "2.1", "Good Brewery", "IPA", "1", "1", "test", "1", False),
        (
            "Good Beer",
            "2",
            "Good Brewery",
            "IPA",
            "1",
            "1",
            "test",
            "1",
            True,
        ),  # ABV Cases
        ("Good Beer", "", "Good Brewery", "IPA", "1", "1", "test", "1", False),
        ("Good Beer", "-1", "Good Brewery", "IPA", "1", "1", "test", "1", False),
        ("Good Beer", "95.424", "Good Brewery", "IPA", "1", "1", "test", "1", True),
        ("Good Beer", "string", "Good Brewery", "IPA", "1", "1", "test", "1", False),
        ("Good Beer", "2.1", "", "IPA", "1", "1", "test", "1", False),  # Brewery Cases
        (
            "Good Beer",
            "2.1",
            "Good Brewery",
            "",
            "",
            "1",
            "test",
            "1",
            False,
        ),  # Style Cases
        (
            "Good Beer",
            "2.1",
            "Good Brewery",
            "IPA",
            "-1",
            "1",
            "test",
            "1",
            False,
        ),  # Vote Cases
        ("Good Beer", "2.1", "Good Brewery", "IPA", "1.01", "1", "test", "1", False),
        ("Good Beer", "2.1", "Good Brewery", "IPA", "41", "1", "test", "1", True),
        (
            "Good Beer",
            "2.1",
            "Good Brewery",
            "IPA",
            "1",
            "0",
            "test",
            "1",
            False,
        ),  # Win Cases
        ("Good Beer", "2.1", "Good Brewery", "IPA", "1", "-1", "test", "1", False),
        ("Good Beer", "2.1", "Good Brewery", "IPA", "1", "2", "test", "1", False),
        (
            "Good Beer",
            "2.1",
            "Good Brewery",
            "IPA",
            "1",
            "1",
            "notarealuser",
            "1",
            False,
        ),  # User cases
    ),
)
def test_beer_input_validator(
    app, beer_name, beer_abv, brewery, style, votes, win, username, session_id, result
):
    with app.app_context():
        # The test user and session are added in test_session_input_validator
        # Need to make that a "module fixture"?
        request = dict()
        request.update(build_session_request_dict("3", "2020-01-01", "test"))
        request.update(
            build_beer_request_dict(
                beer_name, beer_abv, brewery, style, votes, win, username, 0
            )
        )

        validator = AddSessionFormValidator(request)
        val_result = validator.validate_session()
        assert val_result.success == True
        val_result = validator.validate_beers()

        assert val_result.success == result


def build_win_beer(id):
    return build_beer_request_dict(
        beer_name="Good",
        beer_abv=2.1,
        brewery="Good",
        style="Good",
        votes=2,
        win=1,
        username="test",
        id=id,
    )


def build_lose_beer(id):
    return build_beer_request_dict(
        beer_name="Bad",
        beer_abv=2.1,
        brewery="Good",
        style="Good",
        votes=0,
        win=0,
        username="test",
        id=id,
    )


def test_win_checker(app):

    with app.app_context():
        # Valid case
        request_1 = dict()
        request_1.update(build_session_request_dict("3", "2020-01-01", "test"))
        request_1.update(build_win_beer(0))
        request_1.update(build_lose_beer(1))

        # Multiple Win Beers
        request_2 = dict()
        request_2.update(build_session_request_dict("3", "2020-01-01", "test"))
        request_2.update(build_win_beer(0))
        request_2.update(build_win_beer(1))

        # No Win Beers
        request_3 = dict()
        request_3.update(build_session_request_dict("3", "2020-01-01", "test"))
        request_3.update(build_lose_beer(0))
        request_3.update(build_lose_beer(1))

        # No Beers
        request_4 = dict()
        request_4.update(build_session_request_dict("3", "2020-01-01", "test"))

        for request, result in zip(
            [request_1, request_2, request_3, request_4], [True, False, False, False]
        ):
            validator = AddSessionFormValidator(request)
            val_result = validator.validate_session()
            assert val_result.success == True
            val_result = validator.validate_beers()
            assert val_result.success == result


# (TODO) The parameter length is varying so needs some more thought
def test_add_session(app, test_client):
    test_client.post("/auth/login", data={"username": "test", "password": "test"})

    test_good_payload = {
        "session_id": 2,
        "date": "2020-01-01",
        "host": "test",
        "beer_0": "Good Beer",
        "beer_abv_0": "2.1",
        "brewery_0": "Good Brewery",
        "style_0": "IPA",
        "votes_0": "1",
        "win_0": "1",
        "username_0": "test",
    }

    # Check the simple good payload works
    response = test_client.post("/sessions/add_session", data=test_good_payload)
    assert response.status_code == 302
    assert "sessions/fc2" in response.headers["Location"]

    # Check repeated the playoad does not work
    response = test_client.post("/sessions/add_session", data=test_good_payload)
    assert response.status_code == 200
    assert b"Session already exists" in response.data

    # Check a few of the major empty cases
    test_empty_payload_session = {
        "session_id": "",
        "date": "2020-01-01",
        "host": "test",
    }
    # Check repeated the playoad does not work
    response = test_client.post(
        "/sessions/add_session", data=test_empty_payload_session
    )
    assert response.status_code == 200
    assert b"There needs to be a session id" in response.data

    test_empty_payload_date = {
        "session_id": "3",
        "date": "",
        "host": "test",
    }
    # Check repeated the playoad does not work
    response = test_client.post("/sessions/add_session", data=test_empty_payload_date)
    assert response.status_code == 200
    assert b"There needs to be a date" in response.data

    test_empty_payload_user = {
        "session_id": "3",
        "date": "2020-01-01",
        "host": "",
    }
    # Check repeated the playoad does not work
    response = test_client.post("/sessions/add_session", data=test_empty_payload_user)
    assert response.status_code == 200

    assert b"There needs to be a host" in response.data

    test_empty_payload_beer = {
        "session_id": "3",
        "date": "2020-01-01",
        "host": "test",
    }
    # Check repeated the playoad does not work
    response = test_client.post("/sessions/add_session", data=test_empty_payload_beer)
    assert response.status_code == 200
    assert b"There should be exactly 1 winning beer" in response.data
