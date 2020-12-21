import functools

from flask import (
    abort,
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flask_paginate import Pagination, get_page_parameter
from flight_club import get_app
from flight_club import db
from flight_club.models.models import Beer, Session
from flight_club.auth.views import login_required
from flight_club.sessions.fc_sessions import FCSession
from werkzeug.exceptions import BadRequestKeyError

import datetime
import flight_club.models.db_func as db_func

bp = Blueprint("sessions", __name__, url_prefix="/sessions")


def session_input_validator(session_id, date, host):
    """This function is for validation the inputs for the session portion
    of add session. It will type check and value check.

    Args:
        session_id : the id of the session
        date : the date of the session
        host : the host of the

    Returns:
        boolean indicating if checks failed
        error string, either error or None
        session object or None if errors

    """
    # Session id checks
    try:
        session_id = int(session_id)
    except:
        return False, "Session_id needs to be a positive integer", None

    if db_func.check_if_session_exists(session_id):
        return False, "Session already exists", None

    if session_id <= 0:
        return False, "Session id should be a positive number, greater than 0", None

    # Date checks
    # Note date is passed as YYYY-MM-DD we want to store and display MM/DD/YYYY.
    # Mostly because we are dumb Americans.
    try:
        date_object = datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        # This should never happen, since we use a date input selector.
        # Maybe on day someone will attempt to hack us via the date field?
        return False, "Date was not inputted in YYYY-MM-DD format", None

    date = datetime.date.strftime(date_object, "%m/%d/%Y")

    # Host checks
    if not db_func.check_if_user_exists(host):
        return False, "Username {} does not exist".format(host), None

    return True, None, Session(id=session_id, date=date)


def beer_input_validator(
    beer_name, beer_abv, brewery, style, votes, win, username, session_id
):
    """This function is for validating the input from the beer add session form.
    It checks that a few database constraints are met prior to adding,
    as well as values are in the correct format.

    Args:
        beer_name : The string for the beer name.
        beer_abv : A string that will be converted to abv.
        brewery : A string that is the name of the brewery.
        style : A string that is the style of the beer.
        votes : The number of votes this beer got.
        win : An integer that represents if the beer won the session.
        username : The user who brought the beer
        session_id : The session the beer is in

    Returns:
        boolean indicating if checks failed
        error string, either error or None
        beer object or None if errors
    """

    # Checks for beer name.
    if beer_name == "":
        return False, "Beer name should not be an empty string", None

    # Checks for brewery
    if brewery == "":
        return (
            False,
            "Brewery for {} should not be an empty string".format(beer_name),
            None,
        )

    # Checks for abv
    try:
        beer_abv = float(beer_abv)
    except:
        return (
            False,
            "Beer Abv for {} needs to be a valid decimal number".format(beer_abv),
            None,
        )

    if beer_abv < 0:
        return False, "Beer Abv for {} should not be negative".format(beer_abv), None

    # Checks for style
    if style == "":
        return False, "Style for {} should not be an empty string".format(style), None

    # Checks for vote
    try:
        votes = int(votes)
    except:
        return (
            False,
            "Votes for {} should be a valid positive integer".format(votes),
            None,
        )

    if votes < 0:
        return False, "Votes for {} should not be a negative number".format(votes), None

    # Checks for win
    try:
        win = int(win)
    except:
        return False, "Win should be either 1 or 0".format(win), None

    if win < 0 or win > 1:
        return False, "Win should be either 1 or 0".format(win), None

    # Check for username
    if not db_func.check_if_user_exists(username):
        return False, "Username {} does not exist".format(username), None

    # Not validating session here, as it's validated in a different part of the form.
    # Maybe will change this later

    return (
        True,
        None,
        Beer(
            beer_name=beer_name,
            beer_abv=beer_abv,
            brewery=brewery,
            style=style,
            votes=votes,
            win=win,
            username=username,
            session_id=session_id,
        ),
    )


def check_for_winner(beer_list):
    """Checks there is one winner in a list of beers for a session.

    Args:
        beer_list (list[Beer]): list of all beers to be added.

    Returns:
        boolean: True if only one winner, false if no or multiple winners:
    """
    win_count = 0

    for beer in beer_list:
        if beer.win == 1:
            win_count += 1

    if win_count == 1:
        return True
    else:
        return False


@bp.route("/add_session", methods=["GET", "POST"])
@login_required
def add_session():
    if request.method == "POST":
        if not request.form["session_id"]:
            error = "There needs to be a session id"
            flash(error)
            return render_template("sessions/add_session.html")
        if not request.form["date"]:
            error = "There needs to be a date"
            flash(error)
            return render_template("sessions/add_session.html")
        # TODO (dan) I need to actually tie the hosts in.
        if not request.form["host"]:
            error = "There needs to be a host"
            flash(error)
            return render_template("sessions/add_session.html")

        # Check Session isn't duplicate
        session_valid, error, new_session = session_input_validator(
            request.form["session_id"], request.form["date"], request.form["host"]
        )

        if not session_valid:
            flash(error)
            return render_template("sessions/add_session.html")
        else:
            session_id = request.form["session_id"]
            # Construct and add the session
            db.session.add(new_session)

            # Helper variables for beer loop
            still_beers = True
            beer_list = []
            i = 0

            while still_beers:
                try:
                    beer_name = request.form["beer_{}".format(i)]
                    beer_abv = float(request.form["beer_abv_{}".format(i)])
                    brewery = request.form["brewery_{}".format(i)]
                    style = request.form["style_{}".format(i)]
                    votes = request.form["votes_{}".format(i)]
                    win = request.form["win_{}".format(i)]
                    username = request.form["username_{}".format(i)]

                    beer_valid, error, new_beer = beer_input_validator(
                        beer_name,
                        beer_abv,
                        brewery,
                        style,
                        votes,
                        win,
                        username,
                        session_id,
                    )
                    if beer_valid:
                        beer_list.append(new_beer)
                        i += 1
                    else:
                        flash(error)
                        return render_template("sessions/add_session.html")
                except BadRequestKeyError:
                    still_beers = False

            if check_for_winner(beer_list):
                for beer in beer_list:
                    db.session.add(beer)
            else:
                flash("There needs to be exactly one winner.")
                return render_template("sessions/add_session.html")

            # Commit at the end, don't want to commit half things.
            db.session.commit()
            return redirect(url_for("sessions.view_session", id=session_id))

    return render_template("sessions/add_session.html")


@bp.route("/fc<id>", methods=["GET"])
@login_required
def view_session(id):
    # If this isn't a valid session, send a 404.
    if not db_func.check_if_session_exists(id):
        abort(404)
    fc_session = FCSession(int(id))
    return render_template(
        "sessions/session_view.html",
        session_id=fc_session.id,
        date=fc_session.date,
        winner=fc_session.winner,
        beers=fc_session.beers,
        avg_abv=fc_session.session_avg_abv,
    )


@bp.route("/list", methods=["GET"])
@login_required
def list_sessions():

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = current_app.config["POSTS_PER_PAGE"]
    offset = (page - 1) * per_page

    fc_sessions = Session.query.all()
    pagination = Pagination(
        page=page,
        per_page=per_page,
        search=False,
        total=len(fc_sessions),
        record_name="sessions",
        css_framework="bootstrap3",
    )

    return render_template(
        "sessions/session_list.html",
        sessions=fc_sessions[offset : offset + per_page],
        pagination=pagination,
    )
