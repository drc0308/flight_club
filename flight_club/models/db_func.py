import csv
import io

from flask import flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash
from werkzeug.datastructures import FileStorage

from flight_club.models.models import User, Beer, Session
from flight_club import db


def check_if_user_exists(username: str) -> bool:
    """
    Checks to see if a user already exists in the database
    Args:
        username: The user to check for

    Returns:
        True if the user exists in the DB, false otherwise

    """
    if db.session.query(User.query.filter_by(username=username).exists()).scalar():
        return True
    else:
        return False


def add_user(username, password="password"):
    if check_if_user_exists(username):
        return
    db.session.add(User(username=username, password=generate_password_hash(password)))
    db.session.commit()


def check_if_session_exists(session_id):
    if db.session.query(Session.query.filter_by(id=session_id).exists()).scalar():
        return True
    else:
        return False


def add_session(session_id, date):
    if check_if_session_exists(session_id):
        return False
    db.session.add(Session(id=session_id, date=date))
    db.session.commit()


def add_beer(row):
    # CSV Format
    # session, date, username, order, beer, brewery, score, win, specific type, type, abv
    db.session.add(
        Beer(
            beer_name=row[4],
            beer_abv=float(row[10]),
            brewery=row[5],
            style=row[9],
            votes=int(row[6]),
            win=int(row[7]),
            username=row[2],
            session_id=int(row[0]),
        )
    )
    db.session.commit()


def get_beer(beer_name):
    return Beer.query.filter_by(beer_name=beer_name).all()


def csv_add_request(file: FileStorage) -> None:
    """
    Method to edit the underlying CSV that composes the DB from an admin view.
    This reads in a file stream and then updates the database from the streamed
    csv file
    Args:
        file: The stream-able file data coming from Flask

    """
    # store the file contents as a string
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)

    # Skip first row
    next(csv_input)

    for row in csv_input:
        if not check_if_user_exists(row[2]):
            add_user(row[2])
        if not check_if_session_exists(row[0]):
            add_session(row[0], row[1])
        add_beer(row)


def csv_add_filename(filename: str) -> None:
    """
    Reads in a local csv file and generates a DB from the columns
    Args:
        filename: Path to local csv to generate DB from
    """

    with open(filename) as stream:
        csv_input = csv.reader(stream)

        # Skip first row
        next(csv_input)

        for row in csv_input:
            if not check_if_user_exists(row[2]):
                add_user(row[2])
            if not check_if_session_exists(row[0]):
                add_session(row[0], row[1])
            add_beer(row)
