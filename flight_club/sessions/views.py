import functools

from dataclasses import dataclass

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
from sqlalchemy.orm import load_only
from werkzeug.exceptions import BadRequestKeyError

import datetime
import flight_club.models.db_func as db_func

bp = Blueprint("sessions", __name__, url_prefix="/sessions")


@dataclass
class ValidatorResults:
    error: str = ""
    success: bool = False


class AddSessionFormValidator:
    """
    Responsible for taking in the request form and performing necessary input validation.
    """

    def __init__(self, form: dict):
        self._form = form
        self._error = ""
        self._validated = False
        self._session_model = None
        self._beer_model_list = []

    # TODO (dan) if there start to be more forms, consider pullingt these validation
    # functions into a generic validator module.
    @staticmethod
    def _validate_session_id(session_id):
        try:
            session_id = int(session_id)
        except:
            return ValidatorResults("Session_id needs to be a positive integer", False)

        if db_func.check_if_session_exists(session_id):
            return ValidatorResults("Session already exists", False)

        if session_id <= 0:
            return ValidatorResults(
                "Session id should be positve and greater than 0", False
            )

        return ValidatorResults("", True)

    @staticmethod
    def _validate_date(date: str):
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            # This should never happen, since we use a date input selector.
            # Maybe on day someone will attempt to hack us via the date field?
            return ValidatorResults("Date was not inputted in YYYY-MM-DD format", False)

        return ValidatorResults("", True)

    @staticmethod
    def _validate_user(user: str, beer_name=None):
        if not db_func.check_if_user_exists(user):
            if not beer_name:
                return ValidatorResults("User does not exist", False)
            else:
                return ValidatorResults(
                    "User does not exist for {}".format(beer_name), False
                )
        return ValidatorResults("", True)

    @staticmethod
    def _empty_string_validator(value: str, beer_name: str):
        if value == "":
            return ValidatorResults(
                "{} should not be an empty string".format(beer_name), False
            )
        return ValidatorResults("", True)

    @staticmethod
    def _abv_validator(beer_abv: str, beer_name: str):

        try:
            beer_abv = float(beer_abv)
        except:
            return ValidatorResults(
                "ABV for {} should be a floating point num".format(beer_name), False
            )

        if beer_abv < 0:
            return ValidatorResults(
                "ABV for {} should be positive".format(beer_name), False
            )

        return ValidatorResults("", True)

    @staticmethod
    def _votes_validator(votes: str, beer_name: str):
        try:
            votes = int(votes)
        except:
            return ValidatorResults(
                "Votes for {} should be an integer".format(beer_name), False
            )

        if votes < 0:
            return ValidatorResults(
                "Votes for {} should be greater than 0".format(beer_name), False
            )

        return ValidatorResults("", True)

    @staticmethod
    def _win_validator(win: str, beer_name: str):
        try:
            win = int(win)
        except:
            return ValidatorResults(
                "Win for {} should be an integer".format(beer_name), False
            )

        if win < 0 or win > 1:
            return ValidatorResults(
                "Win should be either 0 or 1 for {}".format(beer_name), False
            )

        return ValidatorResults("", True)

    @staticmethod
    def _validate_winner(beer_list):
        win_count = 0

        for beer in beer_list:
            if beer.win == 1:
                win_count += 1

        if win_count == 1:
            return ValidatorResults("", True)
        else:
            return ValidatorResults("There should be exactly 1 winning beer", False)

    def validate_session(self):
        # Confirm all Inputs exist
        if not self._form["session_id"]:
            return ValidatorResults("There needs to be a session id", False)

        if not self._form["date"]:
            return ValidatorResults("There needs to be a date", False)

        # TODO (dan) I need to actually tie the hosts in.
        if not self._form["host"]:
            return ValidatorResults("There needs to be a host", False)

        # Prep for validation
        validator_res = ValidatorResults()
        validator_list = [
            (self._validate_session_id, self._form["session_id"]),
            (self._validate_date, self._form["date"]),
            (self._validate_user, self._form["host"]),
        ]

        # Run validation routines
        for val_func, val_arg in validator_list:
            validator_res = val_func(val_arg)
            if not validator_res.success:
                return validator_res

        # Build the session model
        session_id = int(self._form["session_id"])
        date_object = datetime.datetime.strptime(self._form["date"], "%Y-%m-%d")
        date = datetime.date.strftime(date_object, "%m/%d/%Y")
        self._session_model = Session(id=session_id, date=date)

        return ValidatorResults("", True)

    def validate_beers(self):

        still_beers = True
        while still_beers:
            try:
                i = len(self._beer_model_list)
                beer_name = self._form["beer_{}".format(i)]
                beer_abv = self._form["beer_abv_{}".format(i)]
                brewery = self._form["brewery_{}".format(i)]
                style = self._form["style_{}".format(i)]
                votes = self._form["votes_{}".format(i)]
                win = self._form["win_{}".format(i)]
                username = self._form["username_{}".format(i)]

                val_res = ValidatorResults()
                validator_list = [
                    (self._empty_string_validator, (beer_name, beer_name)),
                    (self._empty_string_validator, (brewery, beer_name)),
                    (self._abv_validator, (beer_abv, beer_name)),
                    (self._empty_string_validator, (style, beer_name)),
                    (self._votes_validator, (votes, beer_name)),
                    (self._win_validator, (win, beer_name)),
                    (self._validate_user, (username, beer_name)),
                ]

                for func, args in validator_list:
                    val_res = func(args[0], args[1])
                    if not val_res.success:
                        return val_res

                self._beer_model_list.append(
                    Beer(
                        beer_name=beer_name,
                        beer_abv=float(beer_abv),
                        brewery=brewery,
                        style=style,
                        votes=int(votes),
                        win=int(win),
                        username=username,
                        session_id=self._session_model.id,
                    )
                )
            except KeyError:
                still_beers = False

        val_res = self._validate_winner(self._beer_model_list)
        if not val_res.success:
            return val_res

        return ValidatorResults("", True)

    @property
    def session_model(self):
        return self._session_model

    @property
    def beer_model_list(self):
        return self._beer_model_list


@bp.route("/add_session", methods=["GET", "POST"])
@login_required
def add_session():
    if request.method == "POST":
        validator = AddSessionFormValidator(request.form)
        session_val_res = validator.validate_session()
        if not session_val_res.success:
            flash(session_val_res.error)
            return render_template("sessions/add_session.html")

        else:
            db.session.add(validator.session_model)
            beer_val_res = validator.validate_beers()

            if not beer_val_res.success:
                flash(beer_val_res.error)
                return render_template("sessions/add_session.html")

            for beer in validator.beer_model_list:
                db.session.add(beer)

            db.session.commit()
            return redirect(
                url_for("sessions.view_session", id=validator.session_model.id)
            )

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


def get_sessions():
    # TODO There has to be a better way to do this conversion...
    fc_sessions = Session.query.options(load_only('id')).all()
    session_list = []
    for session in fc_sessions:
        session_list.append(FCSession(session.id))
    return session_list

@bp.route("/list", methods=["GET"])
@login_required
def list_sessions():

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = current_app.config["POSTS_PER_PAGE"]
    offset = (page - 1) * per_page

    fc_sessions = get_sessions()
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
