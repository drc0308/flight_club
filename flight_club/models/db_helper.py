import csv
import io

from flask import flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash

from flight_club.models.models import User, Beer, Session
from flight_club import db

def check_if_user_exists(username):
    if db.session.query(User.query.filter_by(username=username).exists()).scalar():
        return True
    else:
        return False

def add_user(username):
    db.session.add(User(username=username, password=generate_password_hash('password')))
    db.session.commit()

def check_if_session_exists(session_id):
    if db.session.query(Session.query.filter_by(id=session_id).exists()).scalar():
        return True
    else:
        return False

def add_session(session_id, date):
    db.session.add(Session(id=session_id, date=date))
    db.session.commit()

def add_beer(row):

    # CSV Format
    # session, date, username, order, beer, brewery, score, win, specific type, type
    db.session.add(Beer(
        beer_name=row[4],
        brewery=row[5],
        style=row[9],
        votes=int(row[6]),
        win=int(row[7]),
        username=row[2],
        session_id=int(row[0])
    ))
    db.session.commit()

def csv_add_request(file):
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

def csv_add_filename(filename):
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